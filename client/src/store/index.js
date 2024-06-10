import { createStore } from "vuex";

import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export default createStore({
  state: {
    documents: [],
    user: {},
    accessToken: "",
    results: [],
  },
  mutations: {
    setDocuments(state, payload) {
      state.documents = payload.documents;
    },
    setResults(state, payload) {
      state.results = payload.results;
    },
  },
  actions: {
    loadDocuments(context) {
      return axios.get(`${API_URL}/documents/`).then((response) => {
        context.commit("setDocuments", { documents: response.data });
      });
    },
    uploadDocument(context, formData) {
      return axios
        .post(`${API_URL}/documents/`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          context.commit("setDocuments", { documents: response.data });
        });
    },
    deleteDocument(context, filename) {
      return axios.delete(`${API_URL}/documents/${filename}`);
    },
    runIndexer() {
      return axios.post(`${API_URL}/indexer/`);
    },
    searchDocuments(context, full_text) {
      return axios.post(`${API_URL}/search/${full_text}`).then((response) => {
        context.commit("setResults", { results: response.data });
      });
    },
  },
  getters: {
    results: (state) => state.results,
  },
});
