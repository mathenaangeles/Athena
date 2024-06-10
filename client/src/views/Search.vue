<template>
  <div id="search">
    <el-row>
      <el-alert v-if="error" show-icon type="error">
        {{ error }}
      </el-alert>
      <el-alert v-if="success" show-icon type="success">
        {{ success }}
      </el-alert>
    </el-row>
    <el-row :gutter="10">
      <el-col :md="20">
        <el-input
          id="full-text-input"
          v-model="full_text"
          style="width: 100%"
          placeholder="Search text..."
        >
          <template #prefix>
            <el-icon><Reading /></el-icon>
          </template>
          <template #append>
            <el-button @click="searchIndexer">
              Search
            </el-button>
          </template>
        </el-input>
      </el-col>
      <el-col :md="4">
        <el-button round plain type="primary" @click="runIndexer">
          <el-icon><Document /></el-icon>
          Run Indexer
        </el-button>
      </el-col>
    </el-row>
    <el-row>
      <div v-if="results.length > 0">
        <p v-html="results[0].answer[0]?.highlights"></p>
        <ul>
          <div v-for="(result, title) in results" :key="title">
            <el-card>
              <template #header>
                  <a :href="result.url" target="_blank">{{ result.title }}</a>
              </template>
              <p v-for="caption in result.caption" :key="caption" v-html="caption.highlights"></p>
              <template #footer>   
                 <el-tag>Score: {{result.score}}</el-tag>
                 <el-tag>Reranker Score: {{result.reranker}}</el-tag>
              </template>
            </el-card>
          </div>
        </ul>
      </div>
      <div v-else>
        <el-alert title="No Results Found" type="info" :closable="false"/>
      </div>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "Search",
  data() {
    return {
      full_text: "",
      error: "",
      success: "",
    };
  },
  computed: {
    ...mapGetters(["results"]),
  },
  methods: {
    runIndexer() {
      this.$store
        .dispatch("runIndexer")
        .then(() => {
          this.success = "Indexer has ran successfully.";
          this.error = "";
        })
        .catch((err) => {
          this.error = err;
          this.success = "";
        });
    },
    searchIndexer() {
      this.$store
        .dispatch("searchDocuments", this.full_text)
        .then(() => {
          this.success = "Successfully retrieved relevant documents.";
          this.error = "";
        })
        .catch((err) => {
          this.error = err;
          this.success = "";
        });
    },
  },
};
</script>

<style scoped>
.el-col, .el-row {
  margin-bottom: 10px;
}
.el-card {
  margin: 50px;
}
b {
  color: #67C23A !important;
}
</style>

