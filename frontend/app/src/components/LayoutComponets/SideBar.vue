<template>
  <el-row class="tac">
    <el-col>
      <el-menu
        default-active="2"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
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
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
  PictureFilled,
  Clock,
} from '@element-plus/icons-vue'
const handleOpen = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>
