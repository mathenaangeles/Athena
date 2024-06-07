<template>
  <div id="navbar">
    <el-menu class="navbar-menu" mode="horizontal" :ellipsis="false">
      <div>
        <img
          style="width: 120px"
          src="../assets/text-logo.png"
          alt="Element logo"
        />
      </div>
      <div class="flex-grow"></div>
      <el-menu-item class="menu-item" index="1"
        ><router-link to="/">Search</router-link></el-menu-item
      >
      <el-button @click="login" class="menu-item" type="primary" round
        >Login</el-button
      >
    </el-menu>
  </div>
</template>

<script>
export default {
  name: "Navbar",
  methods: {
    login () {
      this.$store.dispatch('login', { })
        .then(() => this.$router.push('/'))
    },
  },
};
</script>

<style scoped>
.navbar-menu {
  align-items: center;
  padding: 0px 10px;
}
.menu-item {
  margin-left: 5px;
  margin-right: 5px;
}
.flex-grow {
  flex-grow: 1;
}
a {
  text-decoration: none;
}
</style>
