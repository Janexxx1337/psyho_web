<template>
	<div v-if="analysis" class="analysis-section">
		<h3>Анализ настроений</h3>
		<el-card shadow="hover" class="analysis-card">
			<p>{{ analysis }}</p>
		</el-card>
	</div>
</template>

<script setup lang="ts">
	const props = defineProps({
		analysis: {
			type: String,
			required: true,
		},
	});
</script>

<style scoped>
	/* Добавьте стили для MoodAnalysis */
</style>
