<template>
  <el-upload
    action=""
    :before-upload="handleUpload"
    list-type="picture-card"
    :on-preview="handlePictureCardPreview"
    :on-remove="handleRemove"
    :file-list="fileList"
  >
    <el-icon><Plus /></el-icon>
  </el-upload>

  <el-dialog v-model="dialogVisible" width="70%" top="5vh">
    <img w-full :src="dialogImageUrl" alt="Preview Image" />
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import type { UploadProps, UploadUserFile } from 'element-plus'
import { useStore } from '../../store'
import { computed } from 'vue'
const store = useStore()
const URL = computed(() => store.state.URL_PREFIX)

const axios = require('axios').default;
// Optionally the request above could also be done as
var img_list = new Array()
const fileList = ref<UploadUserFile[]>([])
axios.get(URL.value + 'imgs/')
  .then(function (response) {
    const data = response.data
    img_list = new Array(data.length)
    for (var i = 0; i<data.length; i++) { 
      img_list[i] = {
          "name": data[i].id + '-' + data[i].img.split('/')[5],
          "url": data[i].img,
      }
    }
    fileList.value = img_list
  })
  .catch(function (error) {
    console.log(error);
  })
  .then(function () {
    // always executed
  });  
const dialogImageUrl = ref('')
const dialogVisible = ref(false)
const handleUpload = (file) => {
  let formData = new FormData();
    formData.append('img', file);
    const url = 'http://127.0.0.1:8000/imgs/';
    const config = {
        headers: { 'content-type': 'multipart/form-data' }
    }
    axios.post(url, formData, config)
        .then(() => {
            console.log('All Done',);
            axios.get(URL.value + 'imgs/')
              .then(function (response) {
                const data = response.data
                img_list = new Array(data.length)
                for (var i = 0; i<data.length; i++) { 
                  img_list[i] = {
                      "name": data[i].id + '-' + data[i].img.split('/')[5],
                      "url": data[i].img,
                  }
                }
                fileList.value = img_list
              })
  .catch(function (error) {
    console.log(error);
  })
  .then(function () {
    // always executed
  });  
        })
        .catch(error => {
            console.log('error: ', error);
            console.log('error.response: ', error.response);
        });
}
const handleRemove: UploadProps['onRemove'] = (uploadFile, uploadFiles) => {
  console.log(uploadFile, uploadFiles)
  const id = uploadFile.name.split('-')[0]
  console.log(id)
  // Optionally the request above could also be done as
  axios.delete(URL.value + 'imgs/' + id + '/')
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
