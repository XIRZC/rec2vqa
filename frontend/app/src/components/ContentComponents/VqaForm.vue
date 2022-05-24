<template>
  <div style="margin: 10px" />
  <el-form
    label-position="top"
    label-width="100px"
    :model="formData"
    style="max-width: 400px"
  >
    <div style="font-size: 15px; font-weight: bold">
      Step 2: Visual Question Answering (VQA)
    </div>
    <el-form-item label="Question:">
      <el-contianer direction="horizontal" style="width: 400px">
        <el-input v-model="formData.question"
         type="textarea"
         style="max-width: 320px"
         autosize
         clearable
         maxlength="80"
         show-word-limit
         placeholder="Please input a question : )"  />
        <el-button type="primary" @click="vqa_dialog_show = true" style="margin-left: 5px"
          >Submit</el-button
        >
      </el-contianer>
    </el-form-item>
    <el-form-item label="Answer:">
      <el-input v-model="formData.answer" disabled />
    </el-form-item>
  </el-form>
  <el-dialog v-model="vqa_dialog_show" title="Note" width="30%" center draggable>
    <span
      >Confirm to submit vqa form data?
      </span
    >
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="vqa_dialog_show = false">Cancel</el-button>
        <el-button type="primary" @click="onSubmit"
          >Confirm</el-button
        >
      </span>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { useStore } from "../../store";
import { computed } from "vue";
import { reactive, ref } from 'vue'
import { useWebSocket } from "../../hooks";
import { v4 as uuidv4} from 'uuid';
import { ElLoading } from 'element-plus'

const store = useStore()
const last_posted_rec_id = computed(() => store.state.last_rec_post.id)
const URL = computed(() => store.state.URL_PREFIX)
const axios = require('axios');
const vqa_dialog_show = ref(false)
// const ws = useWebSocket(handleOpen, handleMessage);
// function handleOpen (e) {
//   console.log("User connected to the socket with socketid "+ socket_id);
//   ws.send(JSON.stringify({
//     socket_id: socket_id,
//   }));
// };
// function handleMessage (response) {
//   console.log("Getting response from the worker.....");
//   console.log(JSON.parse(response.data));

//   response = JSON.parse(response.data);

//   if ("info" in response){
//     console.log("Info is there as the key");
//   }

//   if ("result" in response){
//     console.log('result come up')
//   }
// };

const formData = reactive({
  question: '',
  answer: '',
  rec: 0,
  socket_id: '',
})

const onSubmit = () => {
  vqa_dialog_show.value = false
  const socket_id = uuidv4()
  formData.rec = last_posted_rec_id.value
  formData.socket_id = socket_id
  axios.post(URL.value + 'vqas/', formData)
    .then( (response) => {
      const query_socket_id = response.data.socket_id
      const loadingInstance = ElLoading.service({
        lock: true,
        text: 'Loading...',
        background: 'rgba(0, 0, 0, 0.7)',
      })
      setTimeout(() => {
        axios.get(URL.value + 'socket', {
          params: {
            socket_id: query_socket_id,
            task: 'vqa',
          }
        })
          .then( (response)  => {
            const data = response.data[0].fields
            formData.answer = data.answer
          })
        loadingInstance.close()
      }, 1000)
    })
    .catch( (error) => {
      console.log(error);
    })
    .then( () => {
    })
}
</script>
