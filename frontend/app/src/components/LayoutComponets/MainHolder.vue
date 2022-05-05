<template>
    <el-container style="padding: 10px 70px">
      <el-container direction="vertical" style="max-width: 400px; text-align: center">
        <ImageHolder />
        <UploadHolder />
      </el-container>
      <el-container direction="vertical" style="max-width: 500px; padding: 5px 30px; height: 420px">
        <el-scrollbar>
          <RecForm />
          <VqaForm />
        </el-scrollbar>
      </el-container>
    </el-container>
</template>

<script>
import ImageHolder from "../ContentComponents/ImageHolder.vue";
import UploadHolder from "../ContentComponents/UploadHolder.vue";
import RecForm from "../ContentComponents/RecForm.vue";
import VqaForm from "../ContentComponents/VqaForm.vue";

export default{
  components: {
    ImageHolder,
    UploadHolder,
    RecForm,
    VqaForm,
  },
};
</script>