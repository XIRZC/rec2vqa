<template>
  <div class="uploader">
    <el-upload
      ref="upload"
      class="upload-demo"
      action=""
      :before-upload="handleUpload"
      :limit="1"
      :on-exceed="handleExceed"
      :auto-upload="false"
    >
      <template #trigger>
        <el-button type="primary">{{select_text}}</el-button>
      </template>
      <el-button class="align" type="success" @click="submitUpload">
        {{upload_text}}
      </el-button>
    </el-upload>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { genFileId } from 'element-plus'
import type { UploadInstance, UploadProps, UploadRawFile } from 'element-plus'
import { useStore } from '../../store'

const upload = ref<UploadInstance>()
const axios = require('axios').default;
const store = useStore()
const URL = computed(() => store.state.URL_PREFIX)
const select_text = computed ( () => store.state.locale[store.state.locale.lang].UploadHolder.select)
const upload_text = computed ( () => store.state.locale[store.state.locale.lang].UploadHolder.upload)

const handleUpload = (file) => {
  let formData = new FormData();
  formData.append('img', file);
  const url = URL.value + 'imgs/';
  console.log('url', url)
  const config = {
      headers: { 'content-type': 'multipart/form-data' }
  }
  axios.post(url, formData, config)
    .then((response) => {
        console.log('response', response);
        store.commit('set_show_img', {
            mode: 'upload',
            data: response.data,
        });
        store.commit('set_has_rec_posted', {
          bin: false,
        });
    })
  .catch(function (error) {
    console.log(error);
  })
  .then(function () {
    // always executed
  });  
}

const handleExceed: UploadProps['onExceed'] = (files) => {
  upload.value!.clearFiles()
  const file = files[0] as UploadRawFile
  file.uid = genFileId()
  upload.value!.handleStart(file)
}

const submitUpload = () => {
  upload.value!.submit()
}
</script>


<style scoped>
.uploader {
  padding: 10px 0;
  text-align: center;
  display: inline-block;
  width: 100%;
  box-sizing: border-box;
  vertical-align: top;
}
.align {
  margin: 0 10px 0
}
</style>
