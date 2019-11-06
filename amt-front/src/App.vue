<template>
  <el-container>
    <el-header>
      <h1>Amazon Mechanical Turk</h1>
    </el-header>
    <el-main>
      <div id="app">
        <router-view />
      </div>
    </el-main>
    <el-footer>
      <h1>NLP*CL Laboratory</h1>
    </el-footer>
  </el-container>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
.el-header,
.el-footer {
  text-align: center;
  background-color: #3f51b5;
  color: #fff;
  height: 96px !important;
  display: flex;
  align-items: center;
  justify-content: center;
}

#app {
  font-family: 'Noto Sans KR', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #4e4e4e;
}

p {
  font-weight: 300;
}

h1 {
  font-weight: 100;
}
</style>
