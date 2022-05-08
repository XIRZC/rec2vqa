import { createStore, useStore as baseUseStore, Store } from 'vuex'
import { InjectionKey } from 'vue'

// define your typings for the store state
export interface Image {
  id: number,
  img: string,
}
export interface ShowImage {
  url: string,
  idx: number,
  list: Array<Image>,
  id: number
}

export interface REC {
  id: number,
  img: number,
  referring_expression: string,
  result: string,
}

export interface State {
  mode: string,
  has_rec_posted: boolean,
  show_img: ShowImage,
  last_rec_post: REC,
}

// define injection key
export const key: InjectionKey<Store<State>> = Symbol()

export const store = createStore<State>({
  state: {
    mode: "Main",  // SideBar menubar set mode, and MainHolder get mode
    has_rec_posted: false,  // MainHolder controller for show vqafrom comp
    show_img: {
      url: '',
      idx: 1,
      list: [],
      id: 1,
    },
    last_rec_post: {
      id: 1,
      img: 1,
      referring_expression: '',
      result: '',
    }
  },
  getters: {
  },
  mutations: {
    set_mode (state, payload) {
      const idx2mode = {
        "1": "Main",
        "2": "Photo",
        "3": "Request",
        "4": "Setting",
      }
      state.mode = idx2mode[payload.index]
      // console.log('store mode', state.mode)
    },
    set_has_rec_posted (state, payload) {
      state.has_rec_posted = payload.bin
      // console.log('has_rec_posted', state.has_rec_posted)
    },
    set_show_img (state, payload) {
      if ( payload.mode === 'next') {
        if ( state.show_img.idx < state.show_img.list.length ) {
          state.show_img.idx ++;
        }
      }
      else if ( payload.mode === 'list' ) {
        state.show_img.list = payload.list;
        // console.log('show_img_list', state.show_img.list)
      }
      else {  // previous
        if ( state.show_img.idx > 1 ) {
          state.show_img.idx --;
        }
      }
      if (state.show_img.list != undefined) {
        state.show_img.url = state.show_img.list[state.show_img.idx-1].img
        state.show_img.id = state.show_img.list[state.show_img.idx-1].id
      }
      // console.log(state.show_img)
    },
    set_last_rec_post (state, payload) {
      const data = payload.data
      state.last_rec_post = {
        id: data.id,
        img: data.img,
        referring_expression: data.referring_expression,
        result: data.result,
      }
      console.log(state.last_rec_post)
      // state.last_rec_post.id = payload.data.id
      // state.last_rec_post.img = payload.data.img
      // state.last_rec_post.referring_expression = payload.data.referring_expression
      // state.last_rec_post.result = payload.data.result
    }
  },
  actions: {
  },
  modules: {
  }
})

// define your own `useStore` composition function
export function useStore () {
  return baseUseStore(key)
}