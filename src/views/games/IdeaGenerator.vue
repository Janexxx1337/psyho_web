<!-- views/games/IdeaGenerator.vue -->
<template>
	<div class="idea-generator">
		<h1>Мозговой штурм и генератор идей</h1>
		<div class="input-section">
			<el-input
				v-model="userProblem"
				placeholder="Введите вашу проблему или ситуацию"
				clearable
			></el-input>
			<el-button type="primary" @click="generateIdeas" :disabled="!userProblem">
				Генерировать идеи
			</el-button>
		</div>

		<div v-if="ideas.length > 0" class="ideas-section">
			<h2>Ваши идеи:</h2>
			<el-collapse accordion>
				<el-collapse-item
					v-for="(idea, index) in ideas"
					:key="index"
					:title="`Идея ${index + 1}`"
				>
					<p>{{ idea }}</p>
				</el-collapse-item>
			</el-collapse>
			<el-button @click="restart" class="restart-button"
				>Начать заново</el-button
			>
		</div>
	</div>
</template>

<script setup lang="ts">
	import { ref } from 'vue';
	import { ElMessage } from 'element-plus';

	const userProblem = ref('');
	const ideas = ref<string[]>([]);

	const methods = [
		'SCAMPER',
		'6 шляп мышления',
		'Случайные ассоциации',
		'Мозговой штурм',
		'Минд-мэппинг',
	];

	const randomWords = [
		'Полет',
		'Вода',
		'Огонь',
		'Музыка',
		'Тишина',
		'Движение',
		'Свет',
		'Тень',
		// Добавьте больше слов
	];

	const generateIdeas = () => {
		ideas.value = [];

		// Используем разные методики для генерации идей
		const selectedMethod = methods[Math.floor(Math.random() * methods.length)];

		switch (selectedMethod) {
			case 'SCAMPER':
				ideas.value.push(...applySCAMPER(userProblem.value));
				break;
			case '6 шляп мышления':
				ideas.value.push(...applySixThinkingHats(userProblem.value));
				break;
			case 'Случайные ассоциации':
				ideas.value.push(...applyRandomAssociations(userProblem.value));
				break;
			case 'Мозговой штурм':
				ideas.value.push(...applyBrainstorming(userProblem.value));
				break;
			case 'Минд-мэппинг':
				ideas.value.push(...applyMindMapping(userProblem.value));
				break;
		}

		ElMessage.success(`Методика: ${selectedMethod}`);
	};

	const applySCAMPER = (problem: string): string[] => {
		return [
			`Заменить: Что если заменить часть проблемы на что-то другое?`,
			`Комбинировать: Можно ли объединить это с чем-то еще?`,
			`Адаптировать: Как можно адаптировать решение из другой области?`,
			`Модифицировать: Что можно изменить в проблеме?`,
			`Применить иначе: Можно ли использовать это по-другому?`,
			`Убрать: Что если убрать часть проблемы?`,
			`Перевернуть: Что если изменить порядок или обратную последовательность?`,
		];
	};

	const applySixThinkingHats = (problem: string): string[] => {
		return [
			`Белая шляпа (факты): Какие факты у нас есть о проблеме?`,
			`Красная шляпа (эмоции): Какие эмоции вызывает эта проблема?`,
			`Черная шляпа (критика): Какие риски и недостатки существуют?`,
			`Желтая шляпа (позитив): Какие преимущества и возможности есть?`,
			`Зеленая шляпа (креативность): Какие новые идеи можно придумать?`,
			`Синяя шляпа (управление): Как мы можем управлять процессом решения?`,
		];
	};

	const applyRandomAssociations = (problem: string): string[] => {
		const word = randomWords[Math.floor(Math.random() * randomWords.length)];
		return [
			`Как "${word}" может помочь решить проблему?`,
			`Какие ассоциации возникают между "${word}" и вашей проблемой?`,
		];
	};

	const applyBrainstorming = (problem: string): string[] => {
		return [
			`Сгенерируйте как можно больше идей, не оценивая их.`,
			`Подумайте об обратных решениях проблемы.`,
		];
	};

	const applyMindMapping = (problem: string): string[] => {
		return [
			`Создайте ментальную карту вокруг проблемы, добавляя связанные идеи.`,
			`Найдите связи между различными аспектами проблемы.`,
		];
	};

	const restart = () => {
		userProblem.value = '';
		ideas.value = [];
	};
</script>

<style scoped>
	.idea-generator {
		padding: 20px;
		max-width: 800px;
		margin: 0 auto;
	}

	.input-section {
		display: flex;
		gap: 10px;
		margin-bottom: 20px;
	}

	.input-section .el-input {
		flex: 1;
	}

	.ideas-section {
		margin-top: 30px;
	}

	.restart-button {
		margin-top: 20px;
	}

	h1,
	h2 {
		text-align: center;
	}

	.el-collapse-item__header {
		font-weight: bold;
	}
</style>
