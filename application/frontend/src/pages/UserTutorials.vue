<template>
  <div>
    <q-table
      flat hide-header wrap-cells
      row-key="title"
      :data="curData"
      :columns="columns"
      :filter="option.value"
      :pagination.sync="pagination"
    >
      <template v-slot:top-left>
        <div class="text-h5 text-bold">My Tutorials</div>
      </template>

      <template v-slot:top-right>
        <q-toolbar>
          <q-select
            outlined dense
            class="q-mr-xs col-4" label="Category Filter"
            bg-color="white" color="black"
            v-model="option"
            style="width: 150px;"
            :options="categories"
          />
        </q-toolbar>
      </template>

      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td colspan="100%" key="title" :props="props">
            <q-card class="q-pa-md" style="min-height: 15vh;">
              <div class="row cursor-pointer">
                <div class="row col" @click="routeToTutorial(props.row)">
                  <div class="col-4 q-pl-md" align="center">
                    <q-img
                      :src="
                        'https://placeimg.com/500/300/nature?t=' + Math.random()
                      "
                      spinner-color="primary"
                      style="max-height: 140px; max-width: 150px"
                    />
                  </div>

                  <div class="col gt-xs">
                    <b>Title:</b>
                    {{ props.row.title }} by {{ props.row.author_username }}<br>

                    <b>Author's Difficulty Rating:</b>
                    {{ props.row.author_difficulty }}<br>

                    <!-- <b>Users' Difficulty Rating:</b>
                    {{ props.row.viewer_difficulty === 'None' ? props.row.author_difficulty : props.row.viewer_difficulty }}<br> -->

                    <b>Users' Rating:</b>
                    <q-rating
                      readonly
                      class="q-pl-sm" size="1.5em" icon="thumb_up"
                      :value="
                        props.row.rating === 'None' ? 5.0 : Number(props.row.rating)
                      "
                    />
                    <br>

                    <b>Category:</b>
                    {{ props.row.category }}<br>
                  </div>

                  <div class="col-5 gt-xs" align="left">
                    <b>Description:</b> {{ props.row.description }}
                  </div>

                  <div class="col xs" align="left">
                    <b>Title:</b>
                    {{ props.row.title }} by {{ props.row.author_username }}
                    <br>

                    <b>Description:</b> {{ props.row.description }}
                  </div>
                </div>

                <div class="col-1" style="
                  display: flex;
                  justify-content: center;
                  align-items: center;"
                >
                  <q-btn
                    round
                    color="primary"
                    @click="invokeDelete(props.row)"
                    icon="delete"
                  />
                </div>
              </div>
            </q-card>
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  created () {
    let username = this.$route.params.username
    let path = `http://54.67.109.241:5000/api/tutorial/${username}`

    if (username === 'admin') {
      path = 'http://54.67.109.241:5000/api/tutorial/get'
    }

    axios.get(path).then(res => {
      if (res.status === 200) {
        this.curData = res.data.tutorials
      }
    })
  },
  data () {
    return {
      filter: '',
      categories: [
        { label: 'Electronics', value: 'electronics' },
        { label: 'Coding', value: 'coding' },
        { label: 'Robotics', value: 'robotics' },
        { label: 'Cooking', value: 'cooking' },
        { label: 'Crafts', value: 'crafts' },
        { label: 'Home & Decor', value: 'homeDecor' },
        { label: 'Testing', value: 'testing' },
        { label: 'All', value: '' }
      ],
      option: '',
      columns: [
        {
          name: 'title',
          label: 'Title',
          required: true,
          align: 'left',
          field: row => row.title,
          format: val => `${val}`,
          sortable: true
        },
        {
          name: 'category',
          label: `Category`,
          required: true,
          align: 'left',
          field: row => row.category,
          format: val => `${val}`,
          sortable: true
        }
      ],
      curData: [],
      pagination: {
        rowsPerPage: 10,
        sortBy: 'title',
        descending: false
      }
    }
  },
  methods: {
    routeToTutorial: function (entry) {
      this.$router.push(`/tutorial/${entry.uuid}`)
    },
    invokeDelete: function (entry) {
      this.$q.dialog({
        title: 'Confirm Delete?',
        persistent: true,
        cancel: true
      }).onOk(() => {
        let path = `http://54.67.109.241:5000/api/tutorial/${entry.uuid}`
        let headers = {
          'x-access-token': this.$q.localStorage.getItem('__diyup__signedIn')
        }

        axios.delete(path, { headers }).then(res => {
          this.curData = this.curData.filter(v => v.uuid !== entry.uuid)
        })
      }).onCancel(() => {
      })
    }
  }
}
</script>

<style>

</style>
