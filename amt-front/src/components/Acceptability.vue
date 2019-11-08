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
            Answer the form below after reading the highlighted sentence:
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
      title:
        'Donald Trump Repeats Calls for Police Profiling After NYC Area Explosions',
      article:
        'One day after explosive devices were discovered in the Manhattan neighborhood of Chelsea and in Seaside Park and Elizabeth in New Jersey, Republican nominee Donald Trump repeated his calls to implement police profiling to stop more attacks in the United States. "Our local police, they know who a lot of these people are. They are afraid to do anything about it because they don\'t want to be accused of profiling and they don\'t want to be accused of all sorts of things," Trump said on "Fox and Friends" when asked what policies he would implement as president to "get tough" on terrorism. He argued that the country had no other choice but to follow the lead of Israel. "Israel has done an unbelievable job, and they will profile. They profile. They see somebody that\'s suspicious," he said, "they will profile. They will take that person in and check out. Do we have a choice? Look what\'s going on. Do we really have a choice? We\'re trying to be so politically correct in our country, and this is only going to get worse." Trump previously made similar comments. After the Orlando nightclub shooting in June, he said in an interview on "Face the Nation" that it was something the U.S. needed to seriously consider.',
      sentence: '"Our local police, they know who a lot of these people are.'
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
    }
  },
  mounted() {
    this.article = this.article.replace(
      this.sentence,
      `<span class='highlight-sentence'>${this.sentence}</span>`
    );
  }
};
</script>

<style>
</style>