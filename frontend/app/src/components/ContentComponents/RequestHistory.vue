<template>
  <div>
    <el-table
      :data="tableData"
      style="width: 100%; margin-bottom: 20px"
      row-key="id"
      border
      default-expand-all
    >
      <el-table-column prop="id" label="ID" />
      <el-table-column prop="referring_expression" label="Referring Expression" />
      <el-table-column prop="result" label="Result" />
      <el-table-column prop="image" label="Image URL" />
    </el-table>
  </div>
</template>
<script lang="ts" setup>
const axios = require('axios');
interface VQA {
  id: number
  question: string
  answer: string
}
interface REC {
  id: number
  referring_expression: string
  result: string
  image: string
  hasChildren?: boolean
  children?: VQA[]
}
// Optionally the request above could also be done as
axios.get('http://region-11.autodl.com:13142/recs/', {
  })
  .then(function (response) {
    console.log(response);
    const tableData: REC[] = [

    ]
  })
  .catch(function (error) {
    console.log(error);
  })
  .then(function () {
    // always executed
  });  
// const tableData: REC[] = [
//   {
//     id: 3,
//     date: '2016-05-01',
//     name: 'wangxiaohu',
//     children: [
//       {
//         id: 31,
//         date: '2016-05-01',
//         name: 'wangxiaohu',
//       },
//     ],
//   },
// ]
</script>