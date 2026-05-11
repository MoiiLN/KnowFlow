import { defineStore } from 'pinia'
import { subscriptionService } from '@/services/api'

interface SubscriptionUsage {
  subscription_plan: string
  flashcards: number
  notes: number
  tasks: number
  knowtionaries: number
}

export const useSubscriptionStore = defineStore('subscription', {
  state: () => ({
    usage: null as SubscriptionUsage | null,
    loading: false,
  }),

  actions: {
    async fetchUsage() {
      this.loading = true

      try {
        const response = await subscriptionService.getUsage()
        this.usage = response.data
      } catch (error) {
        console.error('Error loading subscription usage:', error)
      } finally {
        this.loading = false
      }
    },

    async upgradePlan() {
      try {
        await subscriptionService.upgrade()
        await this.fetchUsage()
      } catch (error) {
        console.error('Error upgrading subscription:', error)
      }
    }
  }
})