<template>
  <div class="app-container">
    <el-card class="filter-container" shadow="never">
      <div>
        <i class="el-icon-search"></i>
        <span>筛选搜索</span>
        <el-button style="float:right" type="primary" @click="handleSearchList()" size="small">
          查询搜索
        </el-button>
        <el-button style="float:right;margin-right: 15px" @click="handleResetSearch()" size="small">
          重置
        </el-button>
      </div>
      <div style="margin-top: 15px">
        <el-form :inline="true" :model="listQuery" size="small" label-width="140px">
          <el-form-item label="kol名称：">
            <el-input v-model="listQuery.kolName" class="input-width" placeholder="kol名称"></el-input>
          </el-form-item>
          <el-form-item label="kol编码：">
            <el-input v-model="listQuery.kolId" class="input-width" placeholder="kol编码"></el-input>
          </el-form-item>
          <el-form-item label="订单时间：">
            <el-date-picker v-model="listQuery.period" type="daterange" range-separator="~" start-placeholder="开始时间"
              end-placeholder="结束时间" />
          </el-form-item>
        </el-form>

      </div>
    </el-card>
    <el-card class="operate-container" shadow="never">
      <i class="el-icon-tickets"></i>
      <span>数据列表</span>
      <el-button size="mini" class="btn-add" @click="addKol">添加</el-button>
    </el-card>

    <div class="table-container">
      <el-table ref="couponTable" :data="list" style="width: 100%;" v-loading="listLoading" border>
        <el-table-column label="编号" width="100" align="center">
          <template slot-scope="scope">{{scope.row.id}}</template>
        </el-table-column>
        <el-table-column label="kol名称" width="100" align="center">
          <template slot-scope="scope">{{scope.row.kolName}}</template>
        </el-table-column>
        <el-table-column label="kol编码" width="100" align="center">
          <template slot-scope="scope">{{scope.row.kolId}}</template>
        </el-table-column>
        <el-table-column label="微信小程序" width="120" align="center">
          <template slot-scope="scope"><img style="height: 80px" :src="scope.row.kolQrCode"></template>
        </el-table-column>
        <el-table-column label="专属超链接" width="400" align="center">
          <template slot-scope="scope">{{scope.row.kolH5Link}}</template>
        </el-table-column>
        <el-table-column label="小程序跳转链接" width="400" align="center">
          <template slot-scope="scope">weixin://dl/business/?appid=wxe26bc51aa1206df9&path=pages/index/index&query=scene%3Dkol_id%3D{{scope.row.kolId}}&env_version={{wxEnv}}</template>
        </el-table-column>
        <el-table-column label="下单量" align="center">
          <template slot-scope="scope">{{scope.row.orderCount|| 0}}</template>
        </el-table-column>
        <el-table-column label="成交订单量" align="center">
          <template slot-scope="scope">{{scope.row.finishOrderCount || 0}}</template>
        </el-table-column>
        <el-table-column label="成交金额" align="center">
          <template slot-scope="scope">{{scope.row.orderAmount|| 0}}</template>
        </el-table-column>
        <el-table-column label="下单人数" align="center">
          <template slot-scope="scope">{{scope.row.userCount|| 0}}</template>
        </el-table-column>
        <el-table-column label="成交人数" align="center">
          <template slot-scope="scope">{{scope.row.finishUserCount|| 0}}</template>
        </el-table-column>
      </el-table>
    </div>
    <div class="pagination-container">
      <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange"
        layout="total, sizes,prev, pager, next,jumper" :current-page.sync="listQuery.pageNum"
        :page-size="listQuery.pageSize" :page-sizes="[5,10,15]" :total="total">
      </el-pagination>
    </div>


    <el-dialog title="添加KOL" :visible.sync="visible" @close="onCancel">
      <el-form>
        <el-form-item label="KOL名称">
          <el-input v-model="kolName" placeholder="请输入KOL名称"></el-input>
        </el-form-item>
        <el-form-item label="KOL ID">
          <el-input v-model="kolId" placeholder="请输入KOL ID"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="onCancel">取消</el-button>
        <el-button type="primary" @click="onConfirm">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import {
    formatDate
  } from '@/utils/date';
  import {
    fetchKol,createKol
  } from '@/api/coupon';
  const defaultListQuery = {
    pageNum: 1,
    pageSize: 10,
    kolName: null,
    kolId: null,
    period: [threeYear(), new Date()]
  };

  function threeYear() {
    const threeYearsAgo = new Date();
    threeYearsAgo.setFullYear(threeYearsAgo.getFullYear() - 2);
    return threeYearsAgo
  }

  export default {
    name: 'kol',
    data() {
      return {
        list: [],
        listLoading: false,
        listQuery: Object.assign({}, defaultListQuery),
        total: 0,
        kolName: null,
        kolId: null,
        visible: false,
        wxEnv:process.env.NODE_ENV == 'development' ?'trial':'release'
      }
    },

    mounted() {
      this.getList()
    },
    methods: {
      onConfirm() {
        createKol({kolId:this.kolId,kolName:this.kolName}).then(resp => {
          if(resp.data) {
            this.visible = false; // 关闭模态框
            this.getList()
          }
        })
      },
      onCancel() {
        this.visible = false; // 关闭模态框
      },
      addKol() {
        this.visible = true; // 打开模态框
      },
      createKol() {
        console.log('create Kol')
      },
      handleSizeChange(val) {
        this.listQuery.pageNum = 1;
        this.listQuery.pageSize = val;
        this.getList();
      },
      handleCurrentChange(val) {
        this.listQuery.pageNum = val;
        this.getList();
      },
      handleResetSearch() {
        this.listQuery = Object.assign({}, defaultListQuery);
      },
      handleSearchList() {
        this.listQuery.pageNum = 1;
        this.getList();
      },
      getList() {
        if (!this.listQuery.period || this.listQuery.period.length != 2) {
          this.listQuery.period = [threeYear(), new Date()]
        }
        this.listQuery.startTime = this.listQuery.period[0]
        this.listQuery.endTime = this.listQuery.period[1]
        fetchKol(this.listQuery).then(resp => {
          this.list = resp.data.list
          this.total = resp.data.total
        })
      },

    }
  }
</script>

<style>
</style>
