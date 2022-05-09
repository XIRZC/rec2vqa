<template>
  <el-row class="tac">
    <el-col>
      <el-menu
        default-active="1"
        class="el-menu-vertical-demo"
        @select="set_mode"
      >
        <el-menu-item index="1">
          <el-icon><icon-menu /></el-icon>
          <span>Main Operator</span>
        </el-menu-item>
        <el-menu-item index="2">
          <el-icon><picture-filled /></el-icon>
          <span>Uploaded Pictures</span>
        </el-menu-item>
        <el-menu-item index="3">
          <el-icon><clock /></el-icon>
          <span>Request History</span>
        </el-menu-item>
        <el-menu-item index="4">
          <el-icon><setting /></el-icon>
          <span>Settings</span>
        </el-menu-item>
      </el-menu>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import { useStore } from '../../store'
import { computed } from 'vue'
import {
  Menu as IconMenu,
  Setting,
  PictureFilled,
  Clock,
} from '@element-plus/icons-vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const store = useStore()

// const mode = computed(() => store.state.mode)
const set_mode = (key, keyPath) => {
  const idx2mode = {
    "1": "Main",
    "2": "Photo",
    "3": "Request",
    "4": "Setting",
  }
  router.push({ name: 'app', params: { mode: idx2mode[key] }})
}
// const set_mode = (key, keyPath) => store.commit('set_mode', {
//   index: key
// })
</script>
