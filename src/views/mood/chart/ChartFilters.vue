<template>
	<el-button-group>
		<el-button @click="$emit('filter', 'week')">
			<span class="material-symbols-outlined">weekend</span>
			Неделя
		</el-button>
		<el-button @click="$emit('filter', 'month')">
			<span class="material-symbols-outlined">calendar_month</span>
			Месяц
		</el-button>
		<el-button @click="$emit('filter', 'all')">
			<span class="material-symbols-outlined">calendar_view_day</span>
			Все
		</el-button>
	</el-button-group>
</template>

<script setup lang="ts"></script>

<style scoped>
	/* Добавьте стили для ChartFilters */
</style>
