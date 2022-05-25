<template>
    <el-container style="font-size: 25px">
        <el-icon style="margin-right: 10px" color="#409EFF"><coffee-cup /></el-icon>
        <block>
            <block style="color: #409EFF;">
              {{header_text}}
            </block>
            <!-- <router-link to="/" style="margin-left: 80px;">{{home_site_name}}</router-link> |
            <router-link to="/about">{{about_site_name}}</router-link> | 
            <router-link :to="{ name: 'app', params: { mode: 'Main' }}" >{{app_site_name}}</router-link> -->
        </block>
    </el-container>
</template>

<script lang="ts" setup>
import { computed } from "vue";
import { useStore } from "../../store";
import {
    CoffeeCup
} from '@element-plus/icons-vue'
const store = useStore()
const header_text = computed(() => store.state.locale[store.state.locale.lang].HeaderBar.header_text)
const home_site_name = computed(() => store.state.locale[store.state.locale.lang].HeaderBar.home_site_name)
const about_site_name = computed(() => store.state.locale[store.state.locale.lang].HeaderBar.about_site_name)
const app_site_name = computed(() => store.state.locale[store.state.locale.lang].HeaderBar.app_site_name)
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
