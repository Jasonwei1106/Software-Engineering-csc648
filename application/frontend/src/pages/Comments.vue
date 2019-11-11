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

    <q-list>
      <q-item
        v-for="(comment, ind) in comments"
        :key="ind"
      >
        <q-item-section>
          <q-item-section avatar>
          <q-avatar>
            <img src="https://cdn.quasar.dev/img/avatar3.jpg">
          </q-avatar>
          </q-item-section>
          <q-item-section>
          <q-item-label lines="1">
            <span style="font-weight:bold; color:#027BE3">{{comment.user}}</span>
          </q-item-label>
          </q-item-section>
          <q-item-label lines="2">
            {{comment.text}}
          </q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
export default {
  data () {
    return {
      reply: '',
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
        this.comments.push({ text: this.reply })
        this.reply = ''
      }
    }
  }
}
</script>
