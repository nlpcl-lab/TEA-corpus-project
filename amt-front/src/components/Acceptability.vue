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
            <b>Annotation Form &mdash; Acceptability ID. {{ this.$route.params.id }}</b>
          </span>
          <el-button style="float: right; margin: -8px;" type="text" @click="help">Help?</el-button>
        </div>
        <div>
          <p>
            Answer the question below.
            <br />Question: Do you accept (or reject) the sentence as true? By true, we mean, the information that you believe in, things that you will tell your friends honestly, without further description.
            Answer the form below after reading the highlighted sentence:
            <br />
            <br />
            <span class="highlight-sentence news-content">{{ sentence }}</span>
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
            <el-form-item label="Reason">
              <el-select v-model="form.reason" placeholder="please select your reason">
                <el-option
                  v-for="reason in reasons[reasonsMap[form.label]]"
                  :label="reason.title"
                  :value="reason.value"
                  :key="reason.title"
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
  name: 'Acceptability',
  data() {
    return {
      form: {
        label: '',
        reason: ''
      },
      options: [
        {
          title: 'Strong Accept',
          desc:
            'I accept the information given by the sentence to be true.\
            I have sound and cogent arguments to justify my acceptance.\
            I am sure that I can effectively convince others that my judgement is reasonable.',
          value: 7
        },
        {
          title: 'Accept',
          desc:
            'I accept the information given by the sentence to be true.\
            I have some arguments to justify my acceptance.\
            But I am not sure whether I can effectively convince others that my judgement is reasonable.',
          value: 6
        },
        {
          title: 'Weak Accept',
          desc:
            'I accept the information given by the sentence to be true.\
            I don’t have arguments justifying my acceptance.\
            Still, I will accept it rather than reject it.',
          value: 5
        },
        {
          title: 'Hard To Judge',
          desc:
            'It is hard to judge whether I should accept or reject the\
            information given by the sentence to be true.',
          value: 4
        },
        {
          title: 'Weak Reject',
          desc:
            'I reject the information given by the sentence to be true.\
            I don’t have arguments for the rejection.\
            Still, I will reject it rather than accept it.',
          value: 3
        },
        {
          title: 'Reject',
          desc:
            'I reject the information given by the sentence to be true,\
            and I have arguments for the rejection.\
            But I am not sure whether I can effectively convince others\
            that my judgement is reasonable.',
          value: 2
        },
        {
          title: 'Strong Reject',
          desc:
            'I reject the information given by the sentence to be true.\
            I have sound and cogent arguments for the rejection.\
            I am sure that I can effectively convince others that my judgement is reasonable.',
          value: 1
        },
        {
          title: 'N/A',
          desc: 'N/A',
          value: 0
        }
      ],
      reasons: [
        [
          {
            title: 'It is a factual information',
            value: 4
          },
          {
            title:
              'It is not a factual information, but I agree with the statement',
            value: 3
          },
          {
            title:
              'It is a subjective statement, but I agree with the statement',
            value: 2
          },
          {
            title: 'It is a reasonable argument',
            value: 1
          },
          {
            title: 'N/A',
            value: 0
          }
        ],
        [
          {
            title: 'It is not a factual information',
            value: 4
          },
          {
            title:
              "It's a subjective statement, therefore I'd neither accept nor reject it",
            value: 3
          },
          {
            title: "I don't have enough information to judge",
            value: 2
          },
          {
            title: 'This sentence gives no information to judge',
            value: 1
          },
          {
            title: 'N/A',
            value: 0
          }
        ],
        [
          {
            title: 'It is not a factual information',
            value: 4
          },
          {
            title:
              "It's a subjective statement, and I do not agree with the statement",
            value: 3
          },
          {
            title:
              'It is not a reasonable argument, and I do not agree with the statement',
            value: 2
          },
          {
            title: 'I do not like the way the author describes the information',
            value: 1
          },
          {
            title: 'N/A',
            value: 0
          }
        ]
      ],
      reasonsMap: {
        7: 0,
        6: 0,
        5: 0,
        4: 1,
        3: 2,
        2: 2,
        1: 2,
        0: 1
      },
      title: '',
      article: '',
      sentence: ''
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
      if (this.form.label.length < 1 || this.form.reason.length < 1) {
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
      db.ref(`acceptability/${this.$route.params.id}`).once(
        'value',
        snapshot => {
          const document = snapshot.val();
          this.title = document.title;
          this.article = document.body;
          this.sentence = document.sentence;

          this.article = this.article.replace(
            this.sentence,
            `<span class='highlight-sentence'>${this.sentence}</span>`
          );
        }
      );
    }
  },
  mounted() {
    this.updateDataAndHighlight();
  }
};
</script>

<style>
</style>