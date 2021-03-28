<template>
  <div class="home">
    <v-list subheader>
      <v-list-item v-for="item in items" :key="item.key" :to="item.key" link>
        <v-list-item-avatar>
          <v-icon class="icon" v-text="item.icon" />
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title v-text="item.title" />
          <v-list-item-subtitle v-text="item.subtitle" />
        </v-list-item-content>
        <v-list-item-icon>
          <v-icon large :color="item.trendColor" v-text="item.trendIcon" />
          <v-list-item-title class="value">
            <pre v-text="item.value" />
          </v-list-item-title>
        </v-list-item-icon>
      </v-list-item>
    </v-list>
    <v-overlay :value="isLoading">
      <v-progress-circular indeterminate size="64" />
    </v-overlay>
  </div>
</template>

<style lang="scss" scoped>
.icon {
  color: black;
  font-style: normal;
}
.value {
  backdrop-filter: blur(1px);
  background: rgba(158, 158, 158, 0.4);
  border-radius: 16px;
  height: 32px;
  line-height: 32px;
  margin-left: -12px;
  position: absolute;
  text-align: center;
  width: 60px;
}
</style>

<script>
import data, { getData, dataItems, dataUnit } from '@/services/data';
import { getValueString } from '@/utils';

export default {
  name: 'Home',
  data: () => ({
    isLoading: false,
    items: [],
  }),
  methods: {
    // 使用非同步的方式取得資料，等待資料時會顯示轉圈圈的動畫
    async getData() {
      this.isLoading = true;
      await getData();
      this.isLoading = false;
    },
    // 設置列表內容
    setItems() {
      for (const dataItem of dataItems) {
        const item = {};
        const last = data.get(dataItem.title)[0];
        const diff = last.value - data.get(dataItem.title)[1].value;
        item.key = dataItem.key;
        item.icon = dataItem.icon;
        item.title = dataItem.title;
        item.subtitle = `${dataUnit}，更新：${last.date}`;
        item.value = getValueString(last.value);
        item.link = dataItem.link;
        // 處理漲幅圖示和顏色
        item.trendColor = 'grey';
        item.trendIcon = 'mdi-trending-neutral';
        if (diff > 0) {
          item.trendColor = 'red';
          item.trendIcon = 'mdi-trending-up';
        } else if (diff < 0) {
          item.trendColor = 'green';
          item.trendIcon = 'mdi-trending-down';
        }
        this.items.push(item);
      }
    },
  },
  created: async function() {
    await this.getData();
    this.setItems();
  },
};
</script>
