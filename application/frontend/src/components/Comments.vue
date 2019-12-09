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
      @click.prevent="sendMes"
      label="send"
    />

    <q-separator />

    <div>
      <q-list>
        <q-item
          v-for="(comment, ind) in comments"
          :key="ind"
        >
          <q-item-section>
            <q-item-label lines="1" class="row">
              <div class="q-py-md">
                <q-avatar>
                  <q-img
                    align= "left"
                    src="https://cdn.quasar.dev/img/avatar3.jpg"
                  />
                </q-avatar>
              </div>

              <div class="q-pa-md">
                <q-item-label lines="1">
                  <p class="text-teal-14 text-bold">
                    {{ comment.username }}
                  </p>
                </q-item-label>
                <q-item-label lines="2" class="q-pl-lg">
                  {{ comment.content }}
                </q-item-label>
              </div>
            </q-item-label>

            <q-item-label lines="2">
              <div class="q-pa-sm">
                <q-btn label="reply" @click.prevent="openReply(ind)" />
              </div>
            </q-item-label>

            <q-item-label lines="3">
              <q-list>
                <q-item
                  v-for="(comment, child_ind) in comments[ind].replies"
                  :key="child_ind"
                >
                  Hello
                </q-item>
              </q-list>
            </q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  created () {
    axios.get(`http://54.153.68.76:5000/api/comments/${this.obj_uuid}/get_all`)
      .then(res => {
        this.data = res.data.comments
        this.data.forEach(element => {
          this.comments.push(
            { ...element }
          )
        })
        // console.log(this.comments)
      })
  },
  props: {
    obj_uuid: String
  },
  data () {
    return {
      data: [],
      reply: '',
      replyMes: '',
      comments: []
    }
  },
  methods: {
    sendMes () {
      // console.log(this.obj_uuid, this.$q.localStorage.getItem('__diyup__signedIn'))
      let headers = {
        'x-access-token': this.$q.localStorage.getItem('__diyup__signedIn')
      }

      if (this.reply !== '') {
        let path = `http://54.153.68.76:5000/api/comments/${this.obj_uuid}/create`
        let body = {
          content: this.reply,
          image: 'test.png'
        }

        axios.post(path, body, { headers })
          .then(res => {
            this.comments.push({
              user: this.$q.localStorage.getItem('__diyup__username'),
              text: this.reply
            })
            this.reply = ''
          })
          .catch(err => {
            if (err) {
              this.$q.notify({
                icon: 'warning',
                color: 'negative',
                message: 'Something went wrong!'
              })
            }
          })
      } else {
        this.$q.notify({
          message: 'put something'
        })
      }
    },
    openReply (index) {
      this.$q.dialog({
        title: 'Enter shit',
        message: 'put stuffs',
        prompt: {
          model: '',
          type: 'text'
        },
        persistent: true,
        cancel: true
      }).onOk(data => {
        // local changes
        this.comments[index].replies.push({
          username: this.$q.localStorage.getItem('__diyup__username'),
          content: `@${this.comments[index].username} ${data}`,
          reply_to: this.comments[index].id
        })
        // TODO: send axios to backend
      }).onCancel(() => {
        // console.log('nothing happens')
      })
    },
    sendReply (index) {
      this.comments[0].reply.push({
        user: this.$q.localStorage.getItem('__diyup__username'),
        text: this.replyMes
      })
      this.replyMes = ''
    }
  }
}
</script>
