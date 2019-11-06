<template>
  <el-row>
    <el-col :span="24" style="text-align: center;">
      <h1>Acceptability &mdash; ID. {{ this.$route.params.id }}</h1>
    </el-col>
    <el-col
      :xs="{span: 24, offset: 0}"
      :sm="{span: 24, offset: 0}"
      :md="{span: 16, offset: 4}"
      :lg="{span: 12, offset: 6}"
      :xl="{span: 10, offset: 7}"
    >
      <el-card class="box-card" shadow="hover">
        <div>
          <p>Hello! hello!</p>
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
            <b>Annotation Form</b>
          </span>
          <el-button style="float: right; margin: -8px;" type="text" @click="help">Help?</el-button>
        </div>
        <div>
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
                  v-for="reason in reasons"
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
        }
      ],
      reasons: [
        {
          title: 'I have seen it before',
          desc: '',
          value: 2
        },
        {
          title: "I don't have any interest",
          desc: '',
          value: 1
        },
        {
          title: 'IDK :(',
          desc: '',
          value: 0
        }
      ]
    };
  },
  methods: {
    help() {
      const h = this.$createElement;
      this.$msgbox({
        title: 'Help',
        message: h(
          'div',
          null,
          this.options.map(x =>
            h('span', null, [
              h('b', null, x.title + ' - '),
              h('span', null, x.desc),
              h('br', null, '')
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
            [h('code', null, JSON.stringify(this.form))]
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
  }
};
</script>

<style>
</style>