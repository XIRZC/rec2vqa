<template>
  <div style="margin: 10px" />
  <el-form
    label-position="top"
    label-width="100px"
    :model="formData"
    style="max-width: 800px"
  >
    <div style="font-size: 15px; font-weight: bold">
      {{title_text}}
    </div>
    <el-form-item :label="question_text">
      <el-contianer direction="horizontal" style="width: 800px">
        <el-input v-model="formData.question"
         type="textarea"
         style="max-width: 640px"
         autosize
         clearable
         maxlength="80"
         show-word-limit
         :placeholder="placeholder_text"  />
        <el-button type="primary" @click="vqa_dialog_show = true" style="margin-left: 5px"
          >{{submit_text}}</el-button
        >
      </el-contianer>
    </el-form-item>
    <el-form-item :label="answer_text">
      <el-input v-model="formData.answer" disabled />
    </el-form-item>
  </el-form>
  <el-dialog v-model="vqa_dialog_show" width="30%" center draggable>
    <span
      >{{dialog_ensure_text}}
      </span
    >
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="vqa_dialog_show = false">{{dialog_cancel_text}}</el-button>
        <el-button type="primary" @click="onSubmit"
          >{{dialog_confirm_text}}</el-button
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

const title_text = computed( () => store.state.locale[store.state.locale.lang].VqaForm.title)
const question_text = computed( () => store.state.locale[store.state.locale.lang].VqaForm.question)
const placeholder_text = computed( () => store.state.locale[store.state.locale.lang].VqaForm.placeholder)
const submit_text = computed( () => store.state.locale[store.state.locale.lang].VqaForm.submit)
const answer_text = computed( () => store.state.locale[store.state.locale.lang].VqaForm.answer)
const dialog_ensure_text = computed( () => store.state.locale[store.state.locale.lang].VqaForm.dialog_ensure)
const dialog_confirm_text = computed( () => store.state.locale[store.state.locale.lang].VqaForm.dialog_confirm)
const dialog_cancel_text = computed( () => store.state.locale[store.state.locale.lang].VqaForm.dialog_cancel)

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
