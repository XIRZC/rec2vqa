<template>
  <el-header height="40px" class="header">
    <HeaderBar />
  </el-header>
  <router-view/>
</template>

<script lang="ts" setup>
import HeaderBar from './components/LayoutComponets/HeaderBar.vue';
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.header {
  position: relative;
  border-bottom: solid 1px var(--el-border-color);
}
</style>