<template>
  <div id="app">
    <Navbar />
    <div id="page">
      <router-view :key="$route.fullPath" />
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
export default {
  name: "App",
  components: {
    Navbar,
  },
};
</script>

<style>
#app {
  font-family: Inter, "Helvetica Neue", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
#page {
  padding: 20px 20px;
  height: 100vh;
}
.el-icon {
  padding-right: 5px;
  padding-left: 5px;
}
a {
  color: #409eff !important;
}
b {
  color: #67C23A !important;
}
</style>
