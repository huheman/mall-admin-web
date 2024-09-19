<template>
  <el-card class="form-container" shadow="never">
    <el-form :model="productAttr" :rules="rules" ref="productAttrFrom" label-width="150px">

      <el-form-item label="属性名称：" prop="name">
        <el-input v-model="productAttr.name">
          <template #suffix>
            <el-tooltip placement="top">
              <template #content>
                <div style="color: red;">对属性做任何修改，都要修改商品和SKU！才会生效</div>
                <div>小海兽不同商品需要接收不同的属性，也是要在上线前提前沟通。</div>
                <div>目前可选的传给小海兽的信息可以时以下内容 </div>
                <div>nickname(昵称)</div>
                <div>username(用户名)</div>
                <div>password(密码)</div>
                <div>server(区服)</div>
                <div>areaServer(服务器)</div>
                <div>如果一个属性要传给小海兽应该在属性名称后面加上"-{对应的编码}",如 <p style="font-weight: bolder;">登录名-username</p>
                </div>
              </template>
              <i class="el-icon-question" style="cursor: pointer;"></i>
            </el-tooltip>
          </template>
        </el-input>
      </el-form-item>

      <el-form-item label="商品类型：">
        <el-select v-model="productAttr.productAttributeCategoryId" placeholder="请选择">
          <el-option v-for="item in productAttrCateList" :key="item.id" :label="item.name" :value="item.id">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="是否加密显示:">
        <el-radio-group v-model="productAttr.filterType">
          <el-radio :label="0">普通</el-radio>
          <el-radio :label="1">加密</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="能否进行检索:" v-show="false">
        <el-radio-group v-model="productAttr.searchType">
          <el-radio :label="0">不需要检索</el-radio>
          <el-radio :label="1">关键字检索</el-radio>
          <el-radio :label="2">范围检索</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="商品属性关联:" v-show="false">
        <el-radio-group v-model="productAttr.relatedStatus">
          <el-radio :label="1">是</el-radio>
          <el-radio :label="0">否</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="属性是否可选:" v-show="false">
        <el-radio-group v-model="productAttr.selectType">
          <el-radio :label="0">唯一</el-radio>
          <el-radio :label="1">单选</el-radio>
          <el-radio :label="2">复选</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="属性值的录入方式:">
        <el-radio-group v-model="productAttr.inputType">
          <el-radio :label="0">手工录入</el-radio>
          <el-radio :label="1">从下面列表中选择</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="属性值可选值列表:" v-show="productAttr.inputType==1">
        <el-input :autosize="true" type="textarea" v-model="inputListFormat">

        </el-input>
      </el-form-item>
      <el-form-item label="是否只能录入数字:" v-show="productAttr.inputType==0">
        <el-radio-group v-model="productAttr.handAddStatus">
          <el-radio :label="1">是</el-radio>
          <el-radio :label="0">否</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="排序属性：">
        <el-input v-model="productAttr.sort"></el-input>
      </el-form-item>
      <el-form-item label="显示条件:">
        <el-input v-model="productAttr.showCondition">
          <template #suffix>
            <el-tooltip content="显示的条件,不填表示总是显示,多个条件用逗号隔开，横杠区分规格内容,如:直充-国际服,代充-国际服" placement="top">
              <i class="el-icon-question" style="cursor: pointer;"></i>
            </el-tooltip>
          </template>
        </el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit('productAttrFrom')">提交</el-button>
        <el-button v-if="!isEdit" @click="resetForm('productAttrFrom')">重置</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
  import {
    fetchList
  } from '@/api/productAttrCate'
  import {
    createProductAttr,
    getProductAttr,
    updateProductAttr
  } from '@/api/productAttr'

  const defaultProductAttr = {
    filterType: 0,
    handAddStatus: 0,
    inputList: '',
    inputType: 0,
    name: '',
    productAttributeCategoryId: 0,
    relatedStatus: 0,
    searchType: 0,
    selectType: 0,
    sort: 0,
    type: 0
  };
  export default {
    name: "ProductAttrDetail",
    props: {
      isEdit: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        productAttr: Object.assign({}, defaultProductAttr),
        rules: {
          name: [{
              required: true,
              message: '请输入属性名称',
              trigger: 'blur'
            },
            {
              min: 2,
              max: 140,
              message: '长度在 2 到 140 个字符',
              trigger: 'blur'
            }
          ]
        },
        productAttrCateList: null,
        inputListFormat: null
      }
    },
    created() {
      if (this.isEdit) {
        getProductAttr(this.$route.query.id).then(response => {
          this.productAttr = response.data;
          this.inputListFormat = this.productAttr.inputList.replace(/,/g, '\n');
        });
      } else {
        this.resetProductAttr();
      }
      this.getCateList();
    },
    watch: {
      inputListFormat: function(newValue, oldValue) {
        newValue = newValue.replace(/\n/g, ',');
        this.productAttr.inputList = newValue;
      }
    },
    methods: {
      getCateList() {
        let listQuery = {
          pageNum: 1,
          pageSize: 100
        };
        fetchList(listQuery).then(response => {
          this.productAttrCateList = response.data.list;
        });
      },
      resetProductAttr() {
        this.productAttr = Object.assign({}, defaultProductAttr);
        this.productAttr.productAttributeCategoryId = Number(this.$route.query.cid);
        this.productAttr.type = Number(this.$route.query.type);
      },
      onSubmit(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$confirm('是否提交数据', '提示', {
              confirmButtonText: '确定',
              cancelButtonText: '取消',
              type: 'warning'
            }).then(() => {
              if (this.isEdit) {
                updateProductAttr(this.$route.query.id, this.productAttr).then(response => {
                  this.$message({
                    message: '修改成功',
                    type: 'success',
                    duration: 1000
                  });
                  this.$router.back();
                });
              } else {
                createProductAttr(this.productAttr).then(response => {
                  this.$message({
                    message: '提交成功',
                    type: 'success',
                    duration: 1000
                  });
                  this.resetForm('productAttrFrom');
                });
              }
            });

          } else {
            this.$message({
              message: '验证失败',
              type: 'error',
              duration: 1000
            });
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
        this.resetProductAttr();
      }
    },
  }
</script>

<style scoped>

</style>
