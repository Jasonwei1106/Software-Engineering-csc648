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
                    {{ comment.user }}
                  </p>
                </q-item-label>
                <q-item-label lines="2" class="q-pl-lg">
                  {{ comment.text }}
                </q-item-label>
              </div>
            </q-item-label>

            <q-item-label lines="2">
              <div class="q-pa-sm">
                <q-btn label="reply" @click.prevent="openReply" />

                <q-input v-if= "display" v-model="replyMes" />

                <q-btn
                  v-if= "display"
                  class="q-my-sm" label="send"
                  @click.prevent="sendReply"
                />
              </div>
            </q-item-label>
          </q-item-section>

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
      replyMes: '',
      display: false,
      comments: [
        {
          user: 'whoevercomment it',
          text: 'balabla',
          reply: {}
        }
      ]
    }
  },
  methods: {
    sendMes () {
      if (this.reply !== '') {
        this.comments.push({
          user: this.$q.localStorage.getItem('__diyup__username'),
          text: this.reply
        })
        this.reply = ''
      }
    },
    openReply () {
      // this.display = true
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
        console.log('okay was pressed and data is :', data)
      }).onCancel(() => {
        console.log('nothing happens')
      })
    },
    sendReply () {
      console.log(this.replyMes)
      this.comments[0].reply.push({
        user: this.$q.localStorage.getItem('__diyup__username'),
        text: this.replyMes
      })
      this.display = false
      this.replyMes = ''
    }
  }
}
</script>
