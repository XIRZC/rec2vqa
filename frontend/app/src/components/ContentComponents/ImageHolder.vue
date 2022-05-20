<template>
  <div class="demo-image">
    <div class="block">
      <el-image :src="show_img_url" fit="cover" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useStore } from '../../store'
import { computed } from 'vue'
const store = useStore()
const URL = computed(() => store.state.URL_PREFIX)
console.log(URL)
const axios = require('axios');
async function getImgs() {
  try {
    const response = await axios.get(URL.value + 'imgs/');
    const data = response.data
    console.log('data', data)
    store.commit('set_show_img', {
      mode: 'list',
      list: data,
    });
  } catch (error) {
    console.error(error);
  }
}
getImgs()
const show_img_url = computed(() => store.state.show_img.url)
</script>

<style scoped>
.demo-image .block {
  padding: 10px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 100%;
  box-sizing: border-box;
  vertical-align: top;
}
.demo-image .block:last-child {
  border-right: none;
}
.demo-image .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
</style>
