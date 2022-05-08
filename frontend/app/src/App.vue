<template>
    <!-- site header -->
    <el-container class="layout-container-demo">

      <el-header height="40px">
        <HeaderBar />
      </el-header>

      <el-container class="layout-container-demo" style="height: 480px">

        <!-- site sidebar -->
        <el-aside width="200px">
          <el-scrollbar>
            <SideBar />
          </el-scrollbar>
        </el-aside>

        <el-container style="height: 500px; padding: 10px">

        <!-- site main content -->
          <el-main style="height:300px">
            <!-- <el-button>out: {{mode}}</el-button> -->
            <el-scrollbar>
              <MainHolder />
            </el-scrollbar>
          </el-main>

          <!-- site footer -->
          <el-footer height="20px">
            <FooterBar />
          </el-footer>

        </el-container>
      </el-container>
    </el-container>
</template>

<script lang="ts" setup>
import HeaderBar from "./components/LayoutComponets/HeaderBar.vue";
import MainHolder from "./components/LayoutComponets/MainHolder.vue";
import SideBar from "./components/LayoutComponets/SideBar.vue";
import FooterBar from "./components/LayoutComponets/FooterBar.vue";
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.layout-container-demo .el-header {
  position: relative;
  border-bottom: solid 1px var(--el-border-color);
  /* background-color: var(--el-color-primary-light-7);
  color: var(--el-text-color-primary); */
}
.layout-container-demo .el-aside {
  border-right: solid 1px var(--el-border-color);
}
.layout-container-demo .el-main {
  padding: 0;
}
.layout-container-demo .el-footer {
  border-top: solid 1px var(--el-border-color);
}
</style>
