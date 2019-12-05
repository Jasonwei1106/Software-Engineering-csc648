<template>
  <div class ="q-pa-md q-gutter-md">
    <strong>Add your comment</strong>
    <q-input
      filled
      type="textarea"
      v-model="reply"
      maxlength="250"
      placeholder="Leave your comments"
      style="max-width:500px;"
    />
    <q-btn
      @click.prevent="sendmes"
      label="send"
    />

    <q-separator />
    <div>
      <q-list>
        <q-item
          v-for="(comment, ind) in comments"
          :key="ind"
        >

        <div class="row justify-start">
          <div class="q-py-md">
          <q-avatar>
            <q-img
              style="align: left"
              src="https://cdn.quasar.dev/img/avatar3.jpg"
            />
          </q-avatar>
          </div>

          <div class=" q-pa-md">
          <q-item-label lines="1">
            <p style="font-weight:bold; color:#027BE3">{{comment.user}}</p>
          </q-item-label>
          <q-item-label lines="2" style="padding-left:10px">
            {{comment.text}}
          </q-item-label>
          </div>
        </div>

        <div>
          <br>
          <q-btn
            @click.prevent="openreply"
            label="reply"
          />

          <q-input
            id="replybtn"
            v-if=replybtn
            v-model="replymes"
          />
          <q-btn
            class="q-my-sm"
            v-if=replybtn
            label="send"
            @click.prevent="sendreply"
          />
        </div>
        </q-item>
      </q-list>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      reply: '',
      replymes: '',
      replybtn: false,
      comments: [
        {
          user: 'whoevercomment it',
          text: 'balabla'
        }
      ]
    }
  },
  methods: {
    sendmes () {
      if (this.reply !== '') {
        this.comments.push({
          user: this.$q.localStorage.getItem('__diyup__username'),
          text: this.reply
        })
        this.reply = ''
      }
    },
    openreply () {
      this.replybtn = true
    },
    sendreply () {
      this.replybtn = false
      this.replymes = ''
    }
  }
}
</script>
