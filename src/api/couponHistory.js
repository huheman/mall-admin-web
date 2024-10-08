import request from '@/utils/request'
export function fetchList(params) {
  return request({
    url:'/couponHistory/list',
    method:'get',
    params:params
  })
}
export function giveCoupon(couponId,phone) {
  return request({
    url:'/couponHistory/giveCoupon?couponId='+couponId+'&phone='+phone,
    method:'post',
  })
}
