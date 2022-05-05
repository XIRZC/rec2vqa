<template>
  <div class="demo-image">
    <div class="block">
      <!-- <span class="demonstration">{{ fit }}</span> -->
      <el-image :src="url" :fit="fit" />
    </div>
  </div>
</template>

<script lang="ts" setup>
const fit = "cover";
const url =
  "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg";
</script>

<style scoped>
.demo-image .block {
  padding: 20px 0;
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
