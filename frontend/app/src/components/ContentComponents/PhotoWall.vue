<template>
  <el-upload
    action="http://127.0.0.1:8000/imgs/"
    list-type="picture-card"
    :on-preview="handlePictureCardPreview"
    :on-remove="handleRemove"
    :file-list="fileList"
  >
    <el-icon><Plus /></el-icon>
  </el-upload>

  <el-dialog v-model="dialogVisible">
    <img w-full :src="dialogImageUrl" alt="Preview Image" />
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Plus } from '@element-plus/icons-vue'

import type { UploadProps, UploadUserFile } from 'element-plus'
const axios = require('axios').default;
// Optionally the request above could also be done as
axios.get('http://127.0.0.1:8000/imgs/')
  .then(function (response) {
    console.log(response);
    const fileList = ref<UploadUserFile[]>([

    ])
  })
  .catch(function (error) {
    console.log(error);
  })
  .then(function () {
    // always executed
  });  

// const fileList = ref<UploadUserFile[]>([
//   {
//     name: 'food2.jpeg',
//     url: '/images/guide.png',
//   },
// ])

const dialogImageUrl = ref('')
const dialogVisible = ref(false)

const handleRemove: UploadProps['onRemove'] = (uploadFile, uploadFiles) => {
  console.log(uploadFile, uploadFiles)
  // Optionally the request above could also be done as
  axios.post('http://127.0.0.1:8000/imgs/', {
      pk: id,
    })
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    })
    .then(function () {
      // always executed
    });  
}

const handlePictureCardPreview: UploadProps['onPreview'] = (uploadFile) => {
  dialogImageUrl.value = uploadFile.url!
  dialogVisible.value = true
}
</script>
