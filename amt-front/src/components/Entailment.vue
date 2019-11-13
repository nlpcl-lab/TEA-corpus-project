<template>
  <el-row>
    <el-col :span="24" style="text-align: center;">
      <h1 class="news-headline">{{ title }}</h1>
    </el-col>
    <el-col
      :xs="{span: 24, offset: 0}"
      :sm="{span: 24, offset: 0}"
      :md="{span: 20, offset: 2}"
      :lg="{span: 18, offset: 3}"
      :xl="{span: 16, offset: 4}"
    >
      <el-card class="box-card" shadow="hover">
        <div>
          <p class="news-content">
            <span v-html="article"></span>
          </p>
        </div>
      </el-card>
    </el-col>
    <el-col style="margin-bottom: 24px;"></el-col>
    <el-col
      :xs="{span: 24, offset: 0}"
      :sm="{span: 24, offset: 0}"
      :md="{span: 16, offset: 4}"
      :lg="{span: 12, offset: 6}"
      :xl="{span: 10, offset: 7}"
    >
      <el-card class="box-card" shadow="hover">
        <div slot="header" class="clearfix">
          <span>
            <b>Annotation Form &mdash; Entailment ID. {{ this.$route.params.id }}</b>
          </span>
          <el-button style="float: right; margin: -8px;" type="text" @click="help">Help?</el-button>
        </div>
        <div>
          <p>
            Answer the question below.
            <br />
            <b>Question</b>: Does Sentence 1 imply Sentence 2?
            <br />
            <br />Sentence 1:
            <span class="highlight-sentence news-content">{{ sentence }}</span>
            <br />Sentence 2:
            <span class="highlight-hypothesis news-content">{{ hypothesis }}</span>
          </p>
          <el-divider></el-divider>
          <el-form :label-position="'left'" ref="form" :model="form" label-width="120px">
            <el-form-item label="Label">
              <el-select v-model="form.label" placeholder="please select your label">
                <el-option
                  v-for="option in options"
                  :label="option.title"
                  :value="option.value"
                  :key="option.title"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <el-divider></el-divider>
          <el-button style="float: right; margin: -8px;" type="primary" @click="submit">Submit</el-button>
          <br />
        </div>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
import { db } from '../firebase';
export default {
  name: 'Entailment',
  data() {
    return {
      form: {
        label: ''
      },
      options: [
        {
          title: 'Contradiction',
          desc: 'Sentence 1 contradicts Sentence 2.',
          value: 0
        },
        {
          title: 'Entailment',
          desc: 'Sentence 1 entails Sentence 2.',
          value: 1
        },
        {
          title: 'Neutral',
          desc: 'Sentence 1 does not entail nor condradict Sentence 2.',
          value: 2
        }
      ],
      sentence: '',
      hypothesis: '',
      title: '',
      article: ''
    };
  },
  methods: {
    help() {
      const h = this.$createElement;
      this.$msgbox({
        title: 'Help',
        message: h(
          'el',
          null,
          this.options.map(x =>
            h('li', null, [
              h('b', null, x.title + ' - '),
              h('span', null, x.desc)
            ])
          )
        ),
        confirmButtonText: 'OK',
        showCancelButton: false,
        customClass: 'helpbox'
      });
    },
    submit() {
      const h = this.$createElement;
      let message = '';
      if (this.form.label.length < 1) {
        message = h(
          'span',
          { style: 'color: #e91e63' },
          'There are unselected things left.'
        );
      } else {
        message = h('span', null, [
          h(
            'b',
            null,
            'Please copy the code below and paste it to the mturk page.'
          ),
          h('br', null, ''),
          h(
            'pre',
            { class: 'language-javascript', style: 'margin-top: 12px;' },
            [h('code', null, btoa(JSON.stringify(this.form)))]
          )
        ]);
      }
      this.$msgbox({
        title: 'Submit',
        message: message,
        confirmButtonText: 'OK',
        showCancelButton: false,
        customClass: 'submitbox'
      });
    },
    updateDataAndHighlight() {
      db.ref(`entailment/${this.$route.params.id}`).once('value', snapshot => {
        const document = snapshot.val();
        this.title = document.title;
        this.article = document.body;
        this.sentence = document.text;
        this.hypothesis = document.hypothesis;

        this.article = this.article
          .replace(
            this.sentence,
            `<span class='highlight-sentence'>${this.sentence}</span>`
          )
          .replace(
            this.hypothesis,
            `<span class='highlight-hypothesis'>${this.hypothesis}</span>`
          );
      });
    }
  },
  mounted() {
    this.updateDataAndHighlight();
  }
};
</script>

<style>
</style>