<template>
  <div id="documents">
    <el-row>
      <el-alert v-if="error" show-icon type="error">
        {{ error }}
      </el-alert>
      <el-alert v-if="success" show-icon type="success">
        {{ success }}
      </el-alert>
    </el-row>
    <el-row :gutter="3">
      <el-col :md="3">
        <input
          id="fileInput"
          type="file"
          @change="chooseFiles"
          style="display: none"
        />
        <el-button
          @click="document.getElementById('fileInput').click()"
          round
          plain
          class="file-btn"
        >
          <el-icon><Files /></el-icon>
          Choose Files
        </el-button>
      </el-col>
      <el-col :md="3">
        <el-button type="primary" @click="uploadFiles" class="file-btn" round>
          <el-icon><Upload /></el-icon>
          Upload Files
        </el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-tag
        v-for="(file, index) of files"
        :key="index"
        closable
        @close="removeFile(index)"
      >
        {{ file.name }}
      </el-tag>
    </el-row>
    <el-row>
      <el-table :data="filteredDocuments" stripe style="width: 100%">
        <el-table-column label="Name">
          <template #default="scope">
            <a :href="scope.row.url">{{ scope.row.name }}</a>
          </template>
        </el-table-column>
        <el-table-column prop="created_on" label="Created On" />
        <el-table-column prop="size" label="Size (MiB)" width="150" />
        <el-table-column width="250">
          <template #header>
            <el-input v-model="search" placeholder="Search document name..." />
          </template>
          <template #default="scope">
            <el-button
              size="small"
              type="danger"
              round
              plain
              @click="deleteFile(scope.row.name)"
            >
              <el-icon><Delete/></el-icon></el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-row>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "Documents",
  data() {
    return {
      document,
      other: true,
      files: [],
      error: "",
      success: "",
      search: "",
    };
  },
  computed: {
    ...mapState({
      documents: (state) => state.documents,
    }),
    filteredDocuments() {
      return this.documents.filter((document) =>
        document.name.toLowerCase().includes(this.search.toLowerCase())
      );
    },
  },
  methods: {
    removeFile(index) {
      this.files.splice(index, 1);
    },
    deleteFile(filename) {
      this.$store
        .dispatch("deleteDocument", filename)
        .then(() => this.$router.go(this.$router.currentRoute))
        .catch((err) => {
          this.error = err;
          this.success = "";
        });
    },
    chooseFiles(e) {
      let file = e.target.files[0];
      if (this.documents.some((document) => document.name === file.name)) {
        this.error = `A file with the name ${file.name} already exists.`;
      } else {
        this.files.push(file);
        this.error = "";
      }
    },
    uploadFiles() {
      let formData = new FormData();
      this.files.forEach((file) => {
        formData.append("files", file);
      });
      this.$store
        .dispatch("uploadDocument", formData)
        .then(() => {
          this.files = [];
          this.error = "";
          this.success = "The new files have been successfully uploaded.";
        })
        .catch((err) => {
          console.log("ERROR: FAILED TO UPLOAD DOCUMENTS", err);
          this.error = err;
          this.success = "";
        });
    },
  },
  beforeMount() {
    this.$store.dispatch("loadDocuments").catch((err) => {
      this.error = err;
    });
  },
};
</script>

<style scoped>
.file-btn {
  width: 130px;
  margin-bottom: 10px;
}
.el-row {
  margin-bottom: 10px;
}
.el-tag {
  margin: 4px 4px;
}
</style>
