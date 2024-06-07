import { createStore } from "vuex";
import { checkToken } from "@/utils";

import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export default createStore({
  state: {
    user: {},
    token: "",
  },
  mutations: {
    setUser(state, payload) {
      state.user = payload.user;
    },
    setJwtToken(state, payload) {
      localStorage.token = payload.token;
      state.token = payload.token;
    },
  },
  actions: {
    login(context, user) {
      context.commit("setUser", { user });
      return axios
        .post(`${API_URL}/login/`, user)
        .then((response) =>
          context.commit("setToken", { token: response.data })
        )
        .catch((error) => {
          console.log(error);
        });
    },
  },
  getters: {
    isAuthenticated(state) {
      return checkToken(state.token);
    },
  },
});
