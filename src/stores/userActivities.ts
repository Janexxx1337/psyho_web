// src/stores/userActivities.ts
import { defineStore } from 'pinia';
import dayjs from 'dayjs';

interface Activities {
	[date: string]: string[];
}

export const useUserActivitiesStore = defineStore('userActivities', {
	state: () => ({
		activities: {} as Activities,
	}),
	actions: {
		addActivity(date: Date, activity: string) {
			const formattedDate = dayjs(date).format('YYYY-MM-DD');
			if (!this.activities[formattedDate]) {
				this.activities[formattedDate] = [];
			}
			this.activities[formattedDate].push(activity);
		},
	},
});
