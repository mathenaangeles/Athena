import { createRouter, createWebHistory } from "vue-router";
import Search from "../views/Search.vue";
import Documents from "../views/Documents.vue";
import Chat from "../views/Chat.vue";

const routes = [
  {
    path: "/",
    name: "Search",
    component: Search,
  },
  {
    path: "/documents",
    name: "Documents",
    component: Documents,
  },
  {
    path: "/chat",
    name: "Chat",
    component: Chat,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
