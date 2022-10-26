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
const shuffle_img_list = computed(() => store.state.shuffule_img_list)
const axios = require('axios');
const shuffle = function (array) {
  let currentIndex = array.length,  randomIndex;

  // While there remain elements to shuffle.
  while (currentIndex != 0) {

    // Pick a remaining element.
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;

    // And swap it with the current element.
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex], array[currentIndex]];
  }

  return array;
}
async function getImgs() {
  try {
    const response = await axios.get(URL.value + 'imgs/');
    var data = response.data
    console.log('original img list', data)
    if (shuffle_img_list.value) {
      data = shuffle(data)
      console.log('shuffled img list', data)
    }
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
