<template>
  <div class="upload-container">
    <el-button icon='el-icon-upload' size="mini" :style="{background:color,borderColor:color}"
               @click=" dialogVisible=true" type="primary">上传图片
    </el-button>
    <el-dialog append-to-body :visible.sync="dialogVisible">
      <el-upload class="editor-slide-upload"
                 :action="useOss?ossUploadUrl:minioUploadUrl"
                 :data="useOss?dataObj:null"
                 :multiple="true"
                 :file-list="fileList"
                 :show-file-list="true"
                 list-type="picture-card"
                 :on-remove="handleRemove"
                 :on-success="handleSuccess"
                 :before-upload="beforeUpload">
        <el-button size="small" type="primary">点击上传</el-button>
      </el-upload>
      <el-button @click="dialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="handleSubmit">确 定</el-button>
    </el-dialog>
  </div>
</template>

<script>
  import {policy} from '@/api/oss'

  export default {
    name: 'editorSlideUpload',
    props: {
      color: {
        type: String,
        default: '#1890ff'
      }
    },
    data() {
      return {
        dialogVisible: false,
        listObj: {},
        fileList: [],
        dataObj: {
          policy: '',
          signature: '',
          key: '',
          ossaccessKeyId: '',
          dir: '',
          host: ''
        },
        useOss:true, //使用oss->true;使用MinIO->false
        ossUploadUrl: process.env.NODE_ENV == 'development' ?
          'http://mall-entry-point-1704301250797321.oss-cn-guangzhou.oss-accesspoint.aliyuncs.com' :
          "http://prd-1704301250797321.oss-cn-guangzhou.oss-accesspoint.aliyuncs.com",
        minioUploadUrl:'http://localhost:8080/minio/upload',
      }
    },
    methods: {
      checkAllSuccess() {
        return Object.keys(this.listObj).every(item => this.listObj[item].hasSuccess)
      },
      handleSubmit() {
        const arr = Object.keys(this.listObj).map(v => this.listObj[v])
        if (!this.checkAllSuccess()) {
          this.$message('请等待所有图片上传成功 或 出现了网络问题，请刷新页面重新上传！')
          return
        }
        console.log(arr);
        this.$emit('successCBK', arr);
        this.listObj = {};
        this.fileList = [];
        this.dialogVisible = false;
      },
      handleSuccess(response, file) {
        const uid = file.uid;
        const objKeyArr = Object.keys(this.listObj)
        for (let i = 0, len = objKeyArr.length; i < len; i++) {
          if (this.listObj[objKeyArr[i]].uid === uid) {
            this.listObj[objKeyArr[i]].url = this.dataObj.host + '/' + this.dataObj.dir + '/' + this.key;
            if(!this.useOss){
              //不使用oss直接获取图片路径
              this.listObj[objKeyArr[i]].url = response.data.url;
            }
            this.listObj[objKeyArr[i]].hasSuccess = true;
            return
          }
        }
      },
      handleRemove(file) {
        const uid = file.uid;
        const objKeyArr = Object.keys(this.listObj);
        for (let i = 0, len = objKeyArr.length; i < len; i++) {
          if (this.listObj[objKeyArr[i]].uid === uid) {
            delete this.listObj[objKeyArr[i]];
            return
          }
        }
      },
      generateRandomString(length) {
        var result = '';
        var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        var charactersLength = characters.length;
        for (var i = 0; i < length; i++) {
          result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
      },
      beforeUpload(file) {
        const _self = this
        const fileName = file.uid;
        this.listObj[fileName] = {};
        if(!this.useOss){
          //不使用oss不需要获取策略
          this.listObj[fileName] = {hasSuccess: false, uid: file.uid, width: this.width, height: this.height};
          return true;
        }
        return new Promise((resolve, reject) => {
          policy().then(response => {
            this.key = this.generateRandomString(20)+file.name.substring(file.name.lastIndexOf('.'));
            _self.dataObj.policy = response.data.policy;
            _self.dataObj.signature = response.data.signature;
            _self.dataObj.ossaccessKeyId = response.data.accessKeyId;
            _self.dataObj.key = response.data.dir + '/'+this.key;
            _self.dataObj.dir = response.data.dir;
            _self.dataObj.host = response.data.host;
            _self.listObj[fileName] = {hasSuccess: false, uid: file.uid, width: this.width, height: this.height};
            resolve(true)
          }).catch(err => {
            console.log(err)
            reject(false)
          })
        })
      }
    }
  }
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .upload-container .editor-slide-upload{
    margin-bottom: 20px;
  }
</style>
