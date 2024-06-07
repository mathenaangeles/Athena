import { createStore } from "vuex";

import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export default createStore({
  state: {
    documents: [],
  },
  mutations: {
    setDocuments (state, payload) {
      state.documents = payload.documents
    },
  },
  actions: {
    loadDocuments (context) {
      return axios.get(`${API_URL}/documents/`)
        .then((response) => {
          context.commit('setDocuments', { documents: response.data })
        })
    },
    uploadDocuments (document) {
      return axios.post(`${API_URL}/documents/`, document)
    }
  },
  getters: {

  },
});
