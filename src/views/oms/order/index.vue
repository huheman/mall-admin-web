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
        <el-button style="float:right;margin-right: 15px" type="primary" @click="handleDownload()" size="small">
          下载
        </el-button>
      </div>
      <div style="margin-top: 15px">
        <el-form :inline="true" :model="listQuery" size="small" label-width="140px">
          <el-form-item label="输入搜索：">
            <el-input v-model="listQuery.orderSn" class="input-width" placeholder="订单编号"></el-input>
          </el-form-item>
          <el-form-item label="收货人手机号：" v-show="false">
            <el-input v-model="listQuery.receiverKeyword" class="input-width" placeholder="手机号码"></el-input>
          </el-form-item>
          <el-form-item label="下单人手机号：">
            <el-input v-model="listQuery.payerPhone" class="input-width" placeholder="下单人手机号"></el-input>
          </el-form-item>
          <el-form-item label="提交时间：">
            <el-date-picker class="input-width" v-model="listQuery.createTime" value-format="yyyy-MM-dd" type="date"
              placeholder="请选择时间">
            </el-date-picker>
          </el-form-item>
          <el-form-item label="订单状态：">
            <el-select v-model="listQuery.status" class="input-width" placeholder="全部" clearable>
              <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="充值类型：">
            <el-select v-model="listQuery.chargeType" class="input-width" placeholder="全部" clearable>
              <el-option v-for="item in chargeTypeOptions" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="是否删除：">
            <el-select v-model="listQuery.deleteStatus" class="input-width" placeholder="全部" clearable>
              <el-option key="1" label="已删除" value="1"></el-option>
              <el-option key="0" label="未删除" value="0">
              </el-option>
            </el-select>
          </el-form-item>
          <!--<el-form-item label="订单来源：">
            <el-select v-model="listQuery.sourceType" class="input-width" placeholder="全部" clearable>
              <el-option v-for="item in sourceTypeOptions"
                         :key="item.value"
                         :label="item.label"
                         :value="item.value">
              </el-option>
            </el-select>
          </el-form-item> -->
        </el-form>
      </div>
    </el-card>
    <el-card class="operate-container" shadow="never">
      <i class="el-icon-tickets"></i>
      <span>数据列表</span>
    </el-card>
    <div class="table-container">
      <el-table ref="orderTable" :data="list" style="width: 100%;" @selection-change="handleSelectionChange"
        v-loading="listLoading" border>
        <el-table-column type="selection" width="60" align="center"></el-table-column>
        <el-table-column label="标号" width="80" align="center">
          <template slot-scope="scope">{{scope.row.id}}</template>
        </el-table-column>

        <el-table-column label="订单标题" width="180" align="center">
          <template slot-scope="scope">{{formatTitle(scope.row)}}</template>
        </el-table-column>
        <el-table-column label="实付金额" align="center">
          <template slot-scope="scope">{{scope.row.payAmount}}</template>
        </el-table-column>
        <el-table-column label="充值方式" align="center">
          <template
            slot-scope="scope">{{scope.row.moreInfo && formatChargeType(JSON.parse(scope.row.moreInfo).attr)}}</template>
        </el-table-column>
        <el-table-column label="支付方式" width="120" align="center">
          <template slot-scope="scope">{{scope.row.payType | formatPayType}}</template>
        </el-table-column>
        <el-table-column label="订单状态" width="120" align="center">
          <template slot-scope="scope">{{scope.row.status | formatStatus}}</template>
        </el-table-column>
        <el-table-column label="操作" width="300" align="center">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleViewOrder(scope.$index, scope.row)">查看订单</el-button>
            <el-button size="mini" @click="handleCloseOrder(scope.$index, scope.row)"
              v-show="scope.row.status===0">关闭订单</el-button>
            <el-button size="mini" @click="handleDeliveryOrder(scope.$index, scope.row)"
              v-show="scope.row.status===1">订单发货</el-button>
            <el-button size="mini" type="danger" @click="handleRefund(scope.$index, scope.row)"
              v-show="scope.row.status===1">手动退款</el-button>
            <!-- <el-button size="mini" @click="handleViewLogistics(scope.$index, scope.row)"
              v-show="scope.row.status===2||scope.row.status===3">订单跟踪</el-button> -->
            <!-- <el-button size="mini" type="danger" @click="handleDeleteOrder(scope.$index, scope.row)"
              v-show="scope.row.status===4">删除订单</el-button> -->
          </template>
        </el-table-column>
        <el-table-column label="直充结果" width="120" align="center">
          <template slot-scope="scope">{{formatDirectCharge(scope.row)}}</template>
        </el-table-column>
        <el-table-column label="下单人手机号" width="180" align="center">
          <template slot-scope="scope">{{scope.row.moreInfo && JSON.parse(scope.row.moreInfo).payerPhone}}</template>
        </el-table-column>
        <el-table-column label="订单金额" align="center">
          <template slot-scope="scope">￥{{scope.row.totalAmount}}</template>
        </el-table-column>
        <el-table-column label="促销信息" align="center">
          <template slot-scope="scope">{{scope.row.promotionInfo}}</template>
        </el-table-column>
        <el-table-column label="促销减免" align="center">
          <template slot-scope="scope">{{scope.row.promotionAmount}}</template>
        </el-table-column>
        <el-table-column label="优惠券减免" align="center">
          <template slot-scope="scope">{{scope.row.couponAmount}}</template>
        </el-table-column>

        <el-table-column label="订单来源" width="120" align="center">
          <template slot-scope="scope">{{scope.row.sourceType | formatSourceType}}</template>
        </el-table-column>
        <el-table-column label="提交时间" width="180" align="center">
          <template slot-scope="scope">{{scope.row.createTime | formatCreateTime}}</template>
        </el-table-column>
        <el-table-column label="发货时间" width="180" align="center">
          <template slot-scope="scope">{{scope.row.deliveryTime | formatCreateTime}}</template>
        </el-table-column>
        <el-table-column label="是否删除" width="180" align="center">
          <template slot-scope="scope">{{scope.row.deleteStatus | formatDeleteStatus}}</template>
        </el-table-column>
        <el-table-column label="订单编号" width="180" align="center">
          <template slot-scope="scope">{{scope.row.orderSn}}</template>
        </el-table-column>

      </el-table>
    </div>
    <div class="batch-operate-container">
      <el-select size="small" v-model="operateType" placeholder="批量操作">
        <el-option v-for="item in operateOptions" :key="item.value" :label="item.label" :value="item.value">
        </el-option>
      </el-select>
      <el-button style="margin-left: 20px" class="search-button" @click="handleBatchOperate()" type="primary"
        size="small">
        确定
      </el-button>
    </div>
    <div class="pagination-container">
      <el-pagination background @size-change="handleSizeChange" @current-change="handleCurrentChange"
        layout="total, sizes,prev, pager, next,jumper" :current-page.sync="listQuery.pageNum"
        :page-size="listQuery.pageSize" :page-sizes="[5,10,15]" :total="total">
      </el-pagination>
    </div>
    <el-dialog title="关闭订单" :visible.sync="closeOrder.dialogVisible" width="30%">
      <span style="vertical-align: top">操作备注：</span>
      <el-input style="width: 80%" type="textarea" :rows="5" placeholder="请输入内容" v-model="closeOrder.content">
      </el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="closeOrder.dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleCloseOrderConfirm">确 定</el-button>
      </span>
    </el-dialog>
    <logistics-dialog v-model="logisticsDialogVisible"></logistics-dialog>
  </div>
</template>
<script>
  import {
    deliveryOrder,
    fetchList,
    closeOrder,
    deleteOrder,
    refundOrder
  } from '@/api/order'
  import {
    formatDate
  } from '@/utils/date';
  import LogisticsDialog from '@/views/oms/order/components/logisticsDialog';
  const defaultListQuery = {
    pageNum: 1,
    pageSize: 10,
    orderSn: null,
    receiverKeyword: null,
    status: null,
    orderType: null,
    sourceType: null,
    createTime: null,
  };
  export default {
    name: "orderList",
    components: {
      LogisticsDialog
    },
    data() {
      return {
        listQuery: Object.assign({}, defaultListQuery),
        listLoading: true,
        list: null,
        total: null,
        operateType: null,
        multipleSelection: [],
        closeOrder: {
          dialogVisible: false,
          content: null,
          orderIds: []
        },
        chargeTypeOptions: [{
            label: '直充',
            value: '直充'
          },
          {
            label: '代充',
            value: '代充'
          }
        ],
        statusOptions: [{
            label: '待付款',
            value: 0
          },
          {
            label: '待发货',
            value: 1
          },
          // {
          //   label: '已发货',
          //   value: 2
          // },
          {
            label: '已完成',
            value: 3
          },
          {
            label: '已关闭',
            value: 4
          }
        ],
        orderTypeOptions: [{
            label: '正常订单',
            value: 0
          },
          {
            label: '秒杀订单',
            value: 1
          }
        ],
        sourceTypeOptions: [{
            label: 'PC订单',
            value: 0
          },
          {
            label: 'APP订单',
            value: 1
          }
        ],
        operateOptions: [{
            label: "批量发货",
            value: 1
          },
          {
            label: "关闭订单",
            value: 2
          },
          {
            label: "删除订单",
            value: 3
          }
        ],
        logisticsDialogVisible: false
      }
    },
    created() {
      this.getList();
    },
    filters: {
      formatCreateTime(time) {
        if (!time) return ''
        let date = new Date(time);
        return formatDate(date, 'yyyy-MM-dd hh:mm:ss')
      },
      formatDeleteStatus(deleteStatus) {
        if (deleteStatus == 0) {
          return '未删除'
        }
        if (deleteStatus == 1) {
          return '已删除'
        }
      },
      formatPayType(value) {
        if (value === 1) {
          return '支付宝';
        } else if (value === 2) {
          return '微信';
        } else {
          return '未支付';
        }
      },
      formatSourceType(value) {
        if (value === 1) {
          return 'APP订单';
        } else {
          return 'PC订单';
        }
      },
      formatStatus(value) {
        if (value === 1) {
          return '待发货';
        } else if (value === 2) {
          return '已发货';
        } else if (value === 3) {
          return '已完成';
        } else if (value === 4) {
          return '已关闭';
        } else if (value === 5) {
          return '无效订单';
        } else if (value == 6) {
          return '退款中';
        } else if (value == 7) {
          return '已退款'
        } else if (value == 0) {
          return '待付款'
        }
      },
    },
    methods: {
      handleDownload() {
        const queryAsJson = JSON.stringify(this.listQuery);

        // 将序列化的 JSON 字符串作为查询参数添加到 URL 中
        const url = `${process.env.BASE_API}/order/download?query=${encodeURIComponent(queryAsJson)}`;

        // 导航到新的 URL
        window.location.href = url;
      },
      formatTitle(row) {
        if (row.moreInfo) {
          return JSON.parse(row.moreInfo).title
        }
      },
      formatDirectCharge(row) {
        if (row.directChargeStatus == 1) {
          return '充值中'
        } else if (row.directChargeStatus == 3) {
          return '充值失败:' + row.directChargeFailReason
        } else if (row.directChargeStatus == 2) {
          return '充值成功'
        }
      },
      formatChargeType(receiverDetailAddress) {
        if (!receiverDetailAddress) {
          return
        }
        if (receiverDetailAddress.indexOf('直充') >= 0) {
          return '直充'
        }
        if (receiverDetailAddress.indexOf('代充') >= 0) {
          return '代充'
        }
      },
      maskPhoneNumber(phone) {
        if (phone) {
          // 使用 slice 方法提取前 3 位和后 4 位
          const start = phone.slice(0, 3);
          const end = phone.slice(-4);

          // 将中间部分替换为 "**"
          return `${start}**${end}`;
        }
      },
      handleResetSearch() {
        this.listQuery = Object.assign({}, defaultListQuery);
      },
      handleSearchList() {
        this.listQuery.pageNum = 1;
        this.getList();
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      handleViewOrder(index, row) {
        this.$router.push({
          path: '/oms/orderDetail',
          query: {
            id: row.id
          }
        })
      },
      handleCloseOrder(index, row) {
        this.closeOrder.dialogVisible = true;
        this.closeOrder.orderIds = [row.id];
      },
      handleRefund(index, row) {
        this.$prompt('请输入退款说明', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          inputPattern: /.+/,
          inputErrorMessage: '退款说明不能为空'
        }).then((value) => {
          // 用户点击了确定按钮后执行退款操作
          refundOrder(row.id, value.value).then(resp => {
            if (resp.code == 200) {
              this.getList()
              this.$message({
                type: 'success',
                message: resp.data
              });
            } else {
              this.$message({
                type: 'error',
                message: resp.message
              });
            }
          })
        }).catch(() => {
          // 用户点击了取消按钮或者关闭了对话框
          this.$message({
            type: 'info',
            message: '已取消退款'
          });
        });
      },
      handleDeliveryOrder(index, row) {
        let listItem = this.covertOrder(row);
        // this.$router.push({
        //   path: '/oms/deliverOrderList',
        //   query: {
        //     list: [listItem]
        //   }
        // })
        this.$confirm('是否要进行发货操作?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          deliveryOrder([listItem]).then(response => {
            // this.$router.back();
            this.$message({
              type: 'success',
              message: '发货成功!'
            });
            this.getList()
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消发货'
          });
        });
      },
      handleViewLogistics(index, row) {
        this.logisticsDialogVisible = true;
      },
      handleDeleteOrder(index, row) {
        let ids = [];
        ids.push(row.id);
        this.deleteOrder(ids);
      },
      handleBatchOperate() {
        if (this.multipleSelection == null || this.multipleSelection.length < 1) {
          this.$message({
            message: '请选择要操作的订单',
            type: 'warning',
            duration: 1000
          });
          return;
        }
        if (this.operateType === 1) {
          //批量发货
          let list = [];
          for (let i = 0; i < this.multipleSelection.length; i++) {
            if (this.multipleSelection[i].status === 1) {
              list.push(this.covertOrder(this.multipleSelection[i]));
            }
          }
          if (list.length === 0) {
            this.$message({
              message: '选中订单中没有可以发货的订单',
              type: 'warning',
              duration: 1000
            });
            return;
          }
          this.$confirm('是否要进行发货操作?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            deliveryOrder(list).then(response => {
              // this.$router.back();
              this.$message({
                type: 'success',
                message: '发货成功!'
              });
              this.getList()
            });
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消发货'
            });
          });
        } else if (this.operateType === 2) {
          //关闭订单
          this.closeOrder.orderIds = [];
          for (let i = 0; i < this.multipleSelection.length; i++) {
            this.closeOrder.orderIds.push(this.multipleSelection[i].id);
          }
          this.closeOrder.dialogVisible = true;
        } else if (this.operateType === 3) {
          //删除订单
          let ids = [];
          for (let i = 0; i < this.multipleSelection.length; i++) {
            ids.push(this.multipleSelection[i].id);
          }
          this.deleteOrder(ids);
        }
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
      handleCloseOrderConfirm() {
        if (this.closeOrder.content == null || this.closeOrder.content === '') {
          this.$message({
            message: '操作备注不能为空',
            type: 'warning',
            duration: 1000
          });
          return;
        }
        let params = new URLSearchParams();
        params.append('ids', this.closeOrder.orderIds);
        params.append('note', this.closeOrder.content);
        closeOrder(params).then(response => {
          this.closeOrder.orderIds = [];
          this.closeOrder.dialogVisible = false;
          this.getList();
          this.$message({
            message: '修改成功',
            type: 'success',
            duration: 1000
          });
        });
      },
      getList() {
        this.listLoading = true;
        fetchList(this.listQuery).then(response => {
          this.listLoading = false;
          this.list = response.data.list;
          this.total = response.data.total;
        });
      },
      deleteOrder(ids) {
        this.$confirm('是否要进行该删除操作?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          let params = new URLSearchParams();
          params.append("ids", ids);
          deleteOrder(params).then(response => {
            this.$message({
              message: '删除成功！',
              type: 'success',
              duration: 1000
            });
            this.getList();
          });
        })
      },
      covertOrder(order) {
        let address = order.receiverProvince + order.receiverCity + order.receiverRegion + order.receiverDetailAddress;
        let listItem = {
          orderId: order.id,
          orderSn: order.orderSn,
          receiverName: order.receiverName,
          receiverPhone: order.receiverPhone,
          receiverPostCode: order.receiverPostCode,
          address: address,
          deliveryCompany: null,
          deliverySn: null
        };
        return listItem;
      }
    }
  }
</script>
<style scoped>
  .input-width {
    width: 203px;
  }
</style>
