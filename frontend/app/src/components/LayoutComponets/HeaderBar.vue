<template>
    <el-container style="font-size: 25px">
        <el-icon style="margin-right: 10px" color="#409EFF"><coffee-cup /></el-icon>
        <block>
            <block style="color: #409EFF;">
              Referring Expression Comprehension Based Visual Question Answering
            </block>
            <router-link to="/" style="margin-left: 80px;">Home</router-link> |
            <router-link to="/about">About</router-link> | 
            <router-link :to="{ name: 'app', params: { mode: 'Main' }}" >App</router-link>
        </block>
    </el-container>
</template>

<script lang="ts" setup>
import {
    CoffeeCup
} from '@element-plus/icons-vue'
</script>

<style scoped>
a {
  font-weight: bold;
  color: #2c3e50;
}

a.router-link-exact-active {
  color: #409EFF;;
}
</style>
