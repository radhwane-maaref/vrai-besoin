<template>
  <div
    class="min-h-screen bg-[#F8F6F2] px-4 sm:px-6 py-8 font-sans pb-24 overflow-x-hidden no-scrollbar w-full relative"
  >
    <header class="mb-8">
      <h1
        class="text-3xl sm:text-4xl font-serif font-bold text-gray-900 tracking-tight"
      >
        Panneau d'administration
      </h1>
    </header>

    <div class="space-y-8 sm:space-y-12">
      <section>
        <div class="mb-4">
          <h2
            class="text-sm font-bold text-gray-600 uppercase tracking-widest pl-2"
          >
            Impact Global
          </h2>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div
            class="bg-gradient-to-r from-[#5B8C85] to-[#4a736d] rounded-[24px] p-5 sm:p-6 shadow-sm text-white relative flex flex-col justify-between min-h-[160px] w-full"
          >
            <div
              v-if="loadingTotalSaved"
              class="animate-pulse flex flex-col h-full justify-between w-full"
            >
              <div class="flex justify-between w-full">
                <div class="h-4 bg-white/20 rounded w-1/2 mb-2"></div>
                <div class="h-6 bg-white/20 rounded w-20"></div>
              </div>
              <div class="h-10 bg-white/20 rounded w-3/4 mb-4"></div>
              <div class="h-3 bg-white/20 rounded w-1/3"></div>
            </div>

            <template v-else>
              <div
                class="flex flex-col sm:flex-row justify-between items-start gap-3 w-full"
              >
                <div class="w-full sm:w-auto">
                  <h3 class="text-sm font-bold opacity-95">Total Économisé</h3>
                  <p
                    class="text-[11px] opacity-75 mt-0.5 font-medium tracking-wide"
                  >
                    Somme des achats évités confirmés
                  </p>
                </div>

                <div
                  class="flex items-center justify-between sm:justify-end gap-1.5 w-full sm:w-auto"
                >
                  <div class="w-full sm:w-[140px]">
                    <CustomSelect
                      v-model="periodTotalSaved"
                      :options="periodOptions"
                      sizeClass="py-1.5 px-3 h-auto text-xs font-semibold w-full"
                      roundedClass="rounded-xl"
                    />
                  </div>

                  <div class="relative group cursor-help p-1 shrink-0">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-4 w-4 opacity-70 hover:opacity-100 transition-opacity"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                    <div
                      class="absolute right-0 top-6 w-[200px] p-2 bg-gray-900 text-white text-[10px] rounded-lg shadow-xl opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-20"
                    >
                      Seuls les abandons confirmés sont inclus. Exclut les
                      intentions en attente.
                    </div>
                  </div>
                </div>
              </div>

              <div
                class="mt-4 sm:mt-2 flex items-baseline gap-1.5 flex-wrap w-full"
              >
                <h2
                  class="text-4xl sm:text-5xl font-black tracking-tight truncate"
                >
                  {{ splitCurrency(dataTotalSaved?.total_saved).value }}
                </h2>
                <span
                  class="text-sm font-bold opacity-80 uppercase tracking-widest shrink-0"
                >
                  {{ splitCurrency(dataTotalSaved?.total_saved).unit }}
                </span>
              </div>

              <div
                class="mt-4 pt-3 border-t border-white/10 flex flex-wrap justify-between items-center text-xs opacity-90 font-medium w-full"
              >
                <span v-if="dailyAverage">Moyenne : {{ dailyAverage }}</span>
                <span v-else>Calculé sur toute la période</span>
              </div>
            </template>
          </div>

          <div
            class="bg-white rounded-[24px] p-5 sm:p-6 shadow-sm border border-gray-100 flex flex-col justify-between min-h-[160px] w-full"
          >
            <div
              v-if="loadingMasteryRatio"
              class="animate-pulse flex flex-col h-full justify-between w-full"
            >
              <div class="flex justify-between w-full">
                <div class="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
                <div class="h-6 bg-gray-200 rounded w-20"></div>
              </div>
              <div class="h-10 bg-gray-200 rounded w-1/3 mb-4"></div>
              <div class="h-2 bg-gray-200 rounded w-full"></div>
            </div>

            <template v-else>
              <div
                class="flex flex-col sm:flex-row justify-between items-start gap-3 w-full"
              >
                <div class="w-full sm:w-auto">
                  <h3 class="text-sm font-bold text-gray-800">
                    Taux de Résistance
                  </h3>
                  <p
                    class="text-[11px] text-gray-500 mt-0.5 font-medium tracking-wide"
                  >
                    Part des intentions non suivies d'achat
                  </p>
                </div>

                <div
                  class="flex items-center justify-between sm:justify-end gap-1.5 w-full sm:w-auto"
                >
                  <div class="w-full sm:w-[140px]">
                    <CustomSelect
                      v-model="periodMasteryRatio"
                      :options="periodOptions"
                      sizeClass="py-1.5 px-3 h-auto text-xs font-semibold w-full"
                      roundedClass="rounded-xl"
                    />
                  </div>

                  <div class="relative group cursor-help p-1 shrink-0">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-4 w-4 text-gray-400 hover:text-gray-600 transition-colors"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                    <div
                      class="absolute right-0 top-6 w-[200px] p-2 bg-gray-900 text-white text-[10px] rounded-lg shadow-xl opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-20"
                    >
                      Résistance = Intentions abandonnées divisées par le total
                      des intentions clôturées.
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-4 sm:mt-2 w-full">
                <h2
                  class="text-4xl sm:text-5xl font-black tracking-tight text-gray-900 truncate"
                >
                  {{ dataMasteryRatio?.mastery_ratio || 0
                  }}<span class="text-2xl text-gray-400 ml-0.5">%</span>
                </h2>
              </div>

              <div class="mt-4 w-full">
                <div
                  class="h-2.5 w-full flex rounded-full overflow-hidden bg-gray-100"
                >
                  <div
                    class="bg-[#5B8C85] h-full transition-all duration-700 ease-out"
                    :style="{
                      width: `${dataMasteryRatio?.mastery_ratio || 0}%`,
                    }"
                  ></div>
                  <div
                    class="bg-[#F87171] h-full transition-all duration-700 ease-out"
                    :style="{
                      width: `${100 - (dataMasteryRatio?.mastery_ratio || 0)}%`,
                    }"
                  ></div>
                </div>
                <div
                  class="flex justify-between text-[10px] sm:text-xs font-bold mt-2 uppercase tracking-wider"
                >
                  <span class="text-[#5B8C85]"
                    >Résistance ({{
                      dataMasteryRatio?.mastery_ratio || 0
                    }}%)</span
                  >
                  <span class="text-[#F87171]"
                    >Impulsion ({{
                      100 - (dataMasteryRatio?.mastery_ratio || 0)
                    }}%)</span
                  >
                </div>
              </div>
            </template>
          </div>
        </div>
      </section>

      <section
        class="bg-white rounded-[24px] p-4 sm:p-6 shadow-sm border border-gray-100 relative w-full"
      >
        <div
          class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4"
        >
          <h2
            class="text-sm font-bold text-gray-600 uppercase tracking-widest pl-2"
          >
            Répartition par Catégorie
          </h2>
          <div class="flex flex-row items-center gap-2 w-full md:w-auto">
            <div class="flex-1 md:flex-none md:w-[120px]">
              <CustomSelect
                v-model="topNCategory"
                :options="topNOptions"
                sizeClass="py-1.5 px-3 h-auto text-xs font-semibold w-full"
                roundedClass="rounded-xl"
              />
            </div>
            <div class="flex-1 md:flex-none md:w-[140px]">
              <CustomSelect
                v-model="periodCategory"
                :options="periodOptions"
                sizeClass="py-1.5 px-3 h-auto text-xs font-semibold w-full"
                roundedClass="rounded-xl"
              />
            </div>
          </div>
        </div>

        <div
          v-if="loadingCategory"
          class="h-64 flex justify-center items-center"
        >
          <div
            class="animate-spin rounded-full h-6 w-6 border-b-2 border-[#5B8C85]"
          ></div>
        </div>
        <div v-else-if="dataCategory?.total > 0">
          <div
            class="w-full max-w-[240px] sm:max-w-[280px] lg:max-w-[320px] mx-auto aspect-square mb-6 relative"
          >
            <Pie :data="categoryChartData" :options="categoryChartOptions" />
            <div
              class="absolute inset-0 flex items-center justify-center pointer-events-none flex-col"
            >
              <span
                class="text-xs text-gray-400 font-bold uppercase tracking-wider"
                >Total</span
              >
              <span class="text-xl sm:text-2xl font-black text-gray-800">{{
                formatNumber(dataCategory.total)
              }}</span>
            </div>
          </div>

          <div class="space-y-2 text-sm bg-gray-50 rounded-xl p-4 mb-4">
            <div
              v-if="dataCategory.top[0]"
              class="flex justify-between items-center gap-2"
            >
              <div class="flex items-center gap-2 min-w-0">
                <div
                  class="w-2.5 h-2.5 rounded-full shrink-0"
                  :style="{ backgroundColor: getCategoryColor(0) }"
                ></div>
                <span class="font-medium truncate">{{
                  dataCategory.top[0].label
                }}</span>
              </div>
              <span class="font-bold whitespace-nowrap shrink-0">
                {{ formatNumber(dataCategory.top[0].value) }}
                <span class="text-gray-400 font-normal text-xs"
                  >({{ dataCategory.top[0].percent }}%)</span
                >
              </span>
            </div>

            <div
              v-if="dataCategory.top[1]"
              class="flex justify-between items-center gap-2"
            >
              <div class="flex items-center gap-2 min-w-0">
                <div
                  class="w-2.5 h-2.5 rounded-full shrink-0"
                  :style="{ backgroundColor: getCategoryColor(1) }"
                ></div>
                <span class="font-medium truncate">{{
                  dataCategory.top[1].label
                }}</span>
              </div>
              <span class="font-bold whitespace-nowrap shrink-0">
                {{ formatNumber(dataCategory.top[1].value) }}
                <span class="text-gray-400 font-normal text-xs"
                  >({{ dataCategory.top[1].percent }}%)</span
                >
              </span>
            </div>

            <div
              v-if="dataCategory.other.value > 0"
              class="flex justify-between items-center text-gray-500 pt-1 border-t border-gray-200 mt-1"
            >
              <div class="flex items-center gap-2">
                <div
                  class="w-2.5 h-2.5 rounded-full bg-gray-300 shrink-0"
                ></div>
                <span class="font-medium">Autres</span>
              </div>
              <span class="font-bold whitespace-nowrap shrink-0">
                {{ formatNumber(dataCategory.other.value) }}
                <span class="text-gray-400 font-normal text-xs"
                  >({{ dataCategory.other.percent }}%)</span
                >
              </span>
            </div>
          </div>

          <button
            @click="showBottomSheet = true"
            class="w-full py-3 text-[#5B8C85] font-semibold text-center rounded-xl bg-[#5B8C85]/10 hover:bg-[#5B8C85]/15 active:bg-[#5B8C85]/20 transition-colors"
          >
            Voir détails
          </button>
        </div>
        <div v-else class="text-center text-gray-400 text-sm py-10">
          Pas de données pour cette période.
        </div>
      </section>

      <section>
        <div class="mb-4">
          <h2
            class="text-sm font-bold text-gray-600 uppercase tracking-widest pl-2"
          >
            Efficacité de l'IA
          </h2>
        </div>

        <div class="space-y-6">
          <div
            class="bg-white rounded-[24px] shadow-sm border border-gray-100 p-4 sm:p-5 relative border-l-4 w-full"
            :class="bypassMetrics.severity.border"
          >
            <div
              v-if="loadingAiBypass"
              class="absolute inset-0 flex justify-center items-center bg-white/60 backdrop-blur-sm z-10 rounded-[24px]"
            >
              <div
                class="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-400"
              ></div>
            </div>

            <div class="flex flex-col w-full gap-3">
              <div
                class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 w-full"
              >
                <div class="flex items-center gap-1.5 flex-wrap min-w-0">
                  <h3 class="font-bold text-gray-900 text-sm truncate">
                    Bypass des alertes d'incohérence
                  </h3>
                  <div class="relative group cursor-help shrink-0">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-4 w-4 text-gray-400 hover:text-gray-600 transition-colors"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                    <div
                      class="absolute right-0 sm:left-full sm:-ml-2 top-6 w-[220px] p-3 bg-gray-900 text-white text-[11px] rounded-lg shadow-xl opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-20"
                    >
                      <p class="font-bold mb-1">Qu'est-ce qu'un bypass ?</p>
                      L'utilisateur a cliqué sur "Continuer quand même" après
                      que l'IA a signalé une incohérence.
                    </div>
                  </div>
                </div>

                <span
                  class="px-2.5 py-1 text-[10px] font-bold rounded-full uppercase tracking-widest w-max shrink-0"
                  :class="bypassMetrics.severity.chip"
                >
                  {{ bypassMetrics.severity.label }}
                </span>
              </div>

              <p class="text-[11px] text-gray-500 font-medium tracking-wide">
                L'utilisateur a continué malgré l'avertissement IA.
              </p>

              <div class="mt-2 flex items-baseline gap-2 flex-wrap">
                <span class="text-4xl font-black text-gray-900 leading-none">
                  {{ bypassMetrics.bypasses }}
                </span>
                <span
                  v-if="bypassMetrics.safeWarnings > 0"
                  class="text-sm font-semibold text-gray-500"
                >
                  sur {{ bypassMetrics.safeWarnings }} alertes ({{
                    bypassMetrics.rate
                  }}%)
                </span>
                <span v-else class="text-sm font-semibold text-gray-400"
                  >Aucune alerte émise</span
                >
              </div>
            </div>

            <div
              class="mt-5 pt-4 border-t border-gray-100 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 w-full"
            >
              <div class="w-full sm:w-[140px]">
                <CustomSelect
                  v-model="periodAiBypass"
                  :options="periodOptions"
                  sizeClass="py-1 px-2 text-xs font-semibold bg-gray-50 border-transparent text-gray-700 w-full"
                  roundedClass="rounded-lg"
                />
              </div>

              <div
                v-if="
                  periodAiBypass !== 'total' && bypassMetrics.safeWarnings > 0
                "
                class="text-xs font-bold flex items-center gap-1 w-full sm:w-auto"
                :class="bypassMetrics.trendInfo.color"
              >
                <span>{{ bypassMetrics.trendInfo.icon }}</span>
                {{ bypassMetrics.trendInfo.text }}
              </div>
            </div>

            <button
              v-if="bypassMetrics.bypasses > 0"
              @click="showBypassSheet = true"
              class="mt-4 w-full py-2.5 text-sm font-bold rounded-xl bg-gray-50 text-gray-600 hover:bg-gray-100 active:bg-gray-200 transition-colors"
            >
              Voir détails du contournement
            </button>
          </div>

          <div
            class="bg-white rounded-[24px] shadow-sm border border-gray-100 p-4 sm:p-5 relative w-full"
          >
            <div
              v-if="loadingAiChart"
              class="absolute inset-0 flex justify-center items-center bg-white/60 backdrop-blur-sm rounded-[24px] z-10"
            >
              <div
                class="animate-spin rounded-full h-8 w-8 border-b-2 border-[#5B8C85]"
              ></div>
            </div>

            <div
              class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-3 w-full"
            >
              <h3 class="font-bold text-gray-900 truncate">
                Verdict IA vs Décision Finale
              </h3>
              <div class="w-full sm:w-[140px]">
                <CustomSelect
                  v-model="periodAiChart"
                  :options="periodOptions"
                  sizeClass="py-1.5 px-3 h-auto text-xs font-semibold w-full"
                  roundedClass="rounded-xl"
                />
              </div>
            </div>
            <div class="mt-6 flex flex-col gap-4 w-full">
              <div
                v-if="dataAiChart?.verdict_stats?.length > 0"
                class="space-y-4 w-full"
              >
                <div
                  v-for="stat in dataAiChart.verdict_stats"
                  :key="stat.ai_verdict"
                  class="bg-gray-50 rounded-xl p-4 sm:p-5 border border-gray-100"
                >
                  <div class="flex justify-between items-center mb-3">
                    <h4 class="font-bold text-gray-800 text-sm">
                      IA recommande :
                      <span class="text-[#5B8C85]">{{
                        formatAiVerdict(stat.ai_verdict)
                      }}</span>
                    </h4>
                    <span
                      class="text-xs font-semibold text-gray-400 bg-gray-200 px-2 py-0.5 rounded-full"
                      >N = {{ stat.total_n }}</span
                    >
                  </div>

                  <div v-if="stat.total_n > 0" class="text-sm space-y-2">
                    <div class="flex justify-between items-center">
                      <span class="text-gray-600 font-medium"
                        >L'utilisateur a choisir d'acheter</span
                      >
                      <span class="font-bold text-gray-900"
                        >{{ stat.final_bought_count }}
                        <span class="text-xs text-gray-400 font-normal ml-1"
                          >({{
                            calcPercent(stat.final_bought_count, stat.total_n)
                          }}%)</span
                        ></span
                      >
                    </div>
                    <div class="flex justify-between items-center">
                      <span class="text-gray-600 font-medium"
                        >L'utilisateur a choisit d'abandonner</span
                      >
                      <span class="font-bold text-gray-900"
                        >{{ stat.final_abandoned_count }}
                        <span class="text-xs text-gray-400 font-normal ml-1"
                          >({{
                            calcPercent(
                              stat.final_abandoned_count,
                              stat.total_n,
                            )
                          }}%)</span
                        ></span
                      >
                    </div>

                    <div class="mt-3 pt-3 border-t border-gray-200">
                      <button
                        @click="toggleWaitExpanded(stat.ai_verdict)"
                        class="w-full flex justify-between items-center text-[#5B8C85] hover:text-[#4a736d] transition-colors"
                      >
                        <span class="text-xs font-bold"
                          >L'utilisateur a choisi d'attendre" :
                          {{ stat.wait_chosen_count }} ({{
                            calcPercent(stat.wait_chosen_count, stat.total_n)
                          }}%)</span
                        >
                        <svg
                          :class="{
                            'rotate-180': expandedWaits.includes(
                              stat.ai_verdict,
                            ),
                          }"
                          xmlns="http://www.w3.org/2000/svg"
                          class="h-4 w-4 transition-transform"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M19 9l-7 7-7-7"
                          />
                        </svg>
                      </button>

                      <div
                        v-show="expandedWaits.includes(stat.ai_verdict)"
                        class="mt-2 pl-3 ml-1 border-l-2 border-[#5B8C85]/20 space-y-1.5 text-[11px] sm:text-xs"
                      >
                        <div class="flex justify-between text-gray-600">
                          <span>↳ Finalement il a acheté</span>
                          <span class="font-bold"
                            >{{ stat.wait_to_bought_count }}
                            <span class="text-gray-400 font-normal ml-1"
                              >({{
                                calcPercent(
                                  stat.wait_to_bought_count,
                                  stat.wait_chosen_count,
                                )
                              }}%)</span
                            ></span
                          >
                        </div>
                        <div class="flex justify-between text-gray-600">
                          <span>↳ Finalement il a abandonné</span>
                          <span class="font-bold"
                            >{{ stat.wait_to_abandoned_count }}
                            <span class="text-gray-400 font-normal ml-1"
                              >({{
                                calcPercent(
                                  stat.wait_to_abandoned_count,
                                  stat.wait_chosen_count,
                                )
                              }}%)</span
                            ></span
                          >
                        </div>
                      </div>
                    </div>
                  </div>

                  <div v-else class="text-xs text-gray-400 py-2 italic">
                    Aucune intention analysée.
                  </div>
                </div>
              </div>

              <div v-else class="text-center text-gray-400 text-sm py-8">
                Pas de données pour cette période.
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <Teleport to="body">
      <div
        v-if="showBottomSheet"
        class="fixed inset-0 z-[100] flex justify-end sm:justify-center flex-col sm:flex-row sm:items-center p-0 sm:p-4"
      >
        <div
          class="absolute inset-0 bg-black/40 backdrop-blur-sm transition-opacity"
          @click="showBottomSheet = false"
        ></div>
        <div
          class="relative bg-white rounded-t-[32px] sm:rounded-[32px] shadow-2xl w-full sm:w-[90%] sm:max-w-md max-h-[85vh] sm:max-h-[80vh] flex flex-col transform transition-transform animate-slide-up sm:animate-none z-10"
        >
          <div
            class="p-5 flex justify-between items-center border-b border-gray-100"
          >
            <h3 class="font-bold text-lg text-gray-900">
              Toutes les catégories
            </h3>
            <button
              @click="showBottomSheet = false"
              class="bg-gray-100 hover:bg-gray-200 rounded-full p-2 text-gray-600 transition-colors shrink-0"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
          </div>
          <div
            class="overflow-y-auto no-scrollbar p-5 pb-[calc(2rem+env(safe-area-inset-bottom))] sm:pb-6 space-y-4"
          >
            <div
              v-for="(cat, idx) in dataCategory?.all"
              :key="cat.key"
              class="flex items-center gap-3"
            >
              <div
                class="w-3 h-3 rounded-full flex-shrink-0"
                :style="{ backgroundColor: getCategoryColor(idx) }"
              ></div>
              <div class="flex-1 min-w-0">
                <div class="truncate text-sm font-medium text-gray-800">
                  {{ cat.label }}
                </div>
                <div class="w-full bg-gray-100 rounded-full h-1 mt-1">
                  <div
                    class="bg-gray-300 h-1 rounded-full"
                    :style="{ width: cat.percent + '%' }"
                  ></div>
                </div>
              </div>
              <div class="text-right flex-shrink-0 pl-2">
                <div class="text-sm font-bold text-gray-900">
                  {{ formatNumber(cat.value) }}
                </div>
                <div class="text-xs font-semibold text-gray-400">
                  {{ cat.percent }}%
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <Teleport to="body">
      <div
        v-if="showBypassSheet"
        class="fixed inset-0 z-[100] flex justify-end sm:justify-center flex-col sm:flex-row sm:items-center p-0 sm:p-4"
      >
        <div
          class="absolute inset-0 bg-black/40 backdrop-blur-sm transition-opacity"
          @click="showBypassSheet = false"
        ></div>
        <div
          class="relative bg-white rounded-t-[32px] sm:rounded-[32px] shadow-2xl w-full sm:w-[90%] sm:max-w-lg max-h-[85vh] sm:max-h-[80vh] flex flex-col transform transition-transform animate-slide-up sm:animate-none z-10"
        >
          <div
            class="p-4 sm:p-6 flex justify-between items-start sm:items-center gap-4 border-b border-gray-100 shrink-0"
          >
            <div class="flex-1 min-w-0">
              <h3 class="font-bold text-lg sm:text-xl text-gray-900 truncate">
                Détails des Contournements
              </h3>
              <p class="text-xs sm:text-sm text-gray-500 mt-0.5 truncate">
                Catégories les plus problématiques
              </p>
            </div>
            <button
              @click="showBypassSheet = false"
              class="bg-gray-100 hover:bg-gray-200 rounded-full p-2 text-gray-600 transition-colors shrink-0"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-6 w-6"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
          </div>

          <div
            class="overflow-y-auto no-scrollbar p-4 sm:p-6 pb-[calc(2.5rem+env(safe-area-inset-bottom))] sm:pb-8 space-y-6"
          >
            <div
              v-for="(cat, idx) in dataAiBypass?.details?.categories"
              :key="idx"
              class="relative"
            >
              <div class="flex justify-between items-end gap-3 mb-2">
                <div class="flex-1 min-w-0 pr-2">
                  <span
                    class="text-sm font-bold text-gray-800 block truncate"
                    :title="cat.product_category"
                  >
                    {{ cat.product_category }}
                  </span>
                </div>

                <div class="shrink-0 text-right whitespace-nowrap">
                  <span class="text-base font-black text-gray-900">{{
                    cat.count
                  }}</span>
                  <span
                    class="text-[10px] sm:text-xs font-medium text-gray-400 ml-1"
                    >contournements</span
                  >
                </div>
              </div>

              <div class="w-full bg-gray-100 rounded-full h-2">
                <div
                  class="bg-red-400 h-2 rounded-full transition-all duration-700 ease-out"
                  :style="{
                    width: `${(cat.count / bypassMetrics.bypasses) * 100}%`,
                  }"
                ></div>
              </div>
            </div>

            <div
              v-if="!dataAiBypass?.details?.categories?.length"
              class="text-center text-gray-400 py-10 text-sm"
            >
              Aucune donnée détaillée disponible pour cette période.
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import api from "@/services/api";
import CustomSelect from "@/components/shared/CustomSelect.vue";

import { Pie } from "vue-chartjs";
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from "chart.js";
ChartJS.register(Title, Tooltip, Legend, ArcElement);

const showBypassSheet = ref(false);
const showBottomSheet = ref(false);

const periodOptions = [
  { value: "day", label: "Aujourd'hui" },
  { value: "week", label: "Cette semaine" },
  { value: "month", label: "Ce mois-ci" },
  { value: "year", label: "Cette année" },
  { value: "total", label: "Total" },
];

const topNOptions = [
  { value: "5", label: "Top 5" },
  { value: "7", label: "Top 7" },
  { value: "10", label: "Top 10" },
];

const categoryColors = [
  "#5B8C85",
  "#FCD34D",
  "#F87171",
  "#60A5FA",
  "#A78BFA",
  "#34D399",
  "#FB923C",
  "#38BDF8",
  "#F472B6",
  "#A3E635",
  "#C084FC",
  "#2DD4BF",
  "#FB7185",
  "#818CF8",
  "#94A3B8",
  "#E1EBE8",
  "#E879F9",
  "#FBBF24",
  "#4ADE80",
  "#9CA3AF",
];

// Formatting Helpers
const formatNumber = (num) => new Intl.NumberFormat("fr-FR").format(num || 0);
const splitCurrency = (val) => {
  const formatted = new Intl.NumberFormat("fr-FR", {
    minimumFractionDigits: 2,
  }).format(Number(val || 0));
  return { value: formatted, unit: "TND" };
};
const getCategoryColor = (idx) => categoryColors[idx % categoryColors.length];

// ==============================================
// 1A. Local State: Total Saved
// ==============================================
const periodTotalSaved = ref("total");
const dataTotalSaved = ref(null);
const loadingTotalSaved = ref(false);

const fetchTotalSaved = async () => {
  loadingTotalSaved.value = true;
  try {
    const res = await api.get("/admin-api/stats/", {
      params: { period: periodTotalSaved.value },
    });
    dataTotalSaved.value = res.data.global_impact;
  } catch (error) {
    console.error("Erreur Total Saved:", error);
  } finally {
    loadingTotalSaved.value = false;
  }
};

const dailyAverage = computed(() => {
  if (
    !dataTotalSaved.value?.total_saved ||
    periodTotalSaved.value === "total" ||
    periodTotalSaved.value === "day"
  ) {
    return null;
  }
  const total = Number(dataTotalSaved.value.total_saved);
  let days = 1;
  if (periodTotalSaved.value === "week") days = 7;
  if (periodTotalSaved.value === "month") days = 30;
  if (periodTotalSaved.value === "year") days = 365;

  const avg = total / days;
  return (
    new Intl.NumberFormat("fr-FR", {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(avg) + " TND / jour"
  );
});

// ==============================================
// 1B. Local State: Mastery Ratio
// ==============================================
const periodMasteryRatio = ref("total");
const dataMasteryRatio = ref(null);
const loadingMasteryRatio = ref(false);

const fetchMasteryRatio = async () => {
  loadingMasteryRatio.value = true;
  try {
    const res = await api.get("/admin-api/stats/", {
      params: { period: periodMasteryRatio.value },
    });
    dataMasteryRatio.value = res.data.global_impact;
  } catch (error) {
    console.error("Erreur Mastery Ratio:", error);
  } finally {
    loadingMasteryRatio.value = false;
  }
};

// ==============================================
// 2. Local State: Categories
// ==============================================
const periodCategory = ref("total");
const topNCategory = ref("7");
const dataCategory = ref(null);
const loadingCategory = ref(false);

const fetchCategory = async () => {
  loadingCategory.value = true;
  try {
    const res = await api.get("/admin-api/stats/categories/", {
      params: { period: periodCategory.value, top_n: topNCategory.value },
    });
    dataCategory.value = res.data;
  } catch (error) {
    console.error("Erreur Catégories:", error);
  } finally {
    loadingCategory.value = false;
  }
};

const categoryChartData = computed(() => {
  if (!dataCategory.value || dataCategory.value.total === 0)
    return { labels: [], datasets: [] };

  const labels = dataCategory.value.top.map((c) => c.label);
  const data = dataCategory.value.top.map((c) => c.value);
  const bgColors = dataCategory.value.top.map((_, i) => getCategoryColor(i));

  if (dataCategory.value.other.value > 0) {
    labels.push("Autres");
    data.push(dataCategory.value.other.value);
    bgColors.push("#E5E7EB");
  }

  return {
    labels,
    datasets: [
      {
        data,
        backgroundColor: bgColors,
        borderWidth: 2,
        borderColor: "#ffffff",
        hoverOffset: 4,
      },
    ],
  };
});

const categoryChartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  aspectRatio: 1,
  cutout: "60%",
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: "rgba(255, 255, 255, 0.95)",
      titleColor: "#1F2937",
      bodyColor: "#4B5563",
      borderColor: "#E5E7EB",
      borderWidth: 1,
      padding: 10,
      callbacks: {
        label: (ctx) => {
          const val = ctx.raw || 0;
          const percent = ((val / dataCategory.value.total) * 100).toFixed(1);
          return ` ${val} intentions (${percent}%)`;
        },
      },
    },
  },
};

// ==============================================
// 3A. Local State: AI Effectiveness (Bypass)
// ==============================================
const periodAiBypass = ref("total");
const dataAiBypass = ref(null);
const loadingAiBypass = ref(false);

const bypassMetrics = computed(() => {
  const data = dataAiBypass.value || {};
  const bypasses = data.bypasses || 0;

  const safeWarnings = Math.max(data.warnings || 0, bypasses);
  const rate =
    safeWarnings > 0 ? Math.round((bypasses / safeWarnings) * 100) : 0;
  const trend = data.trend_diff || 0;

  let severity = {
    label: "Faible",
    chip: "bg-green-100 text-green-700",
    border: "border-l-[#34D399]",
  };
  if (rate >= 15) {
    severity = {
      label: "Problématique",
      chip: "bg-red-100 text-red-700",
      border: "border-l-[#F87171]",
    };
  } else if (rate >= 5) {
    severity = {
      label: "À surveiller",
      chip: "bg-amber-100 text-amber-700",
      border: "border-l-[#FBBF24]",
    };
  }

  let trendInfo = { text: "Stagnation", color: "text-gray-400", icon: "→" };
  if (trend > 0) {
    trendInfo = {
      text: `+${trend} vs précédent`,
      color: "text-red-500",
      icon: "↗",
    };
  } else if (trend < 0) {
    trendInfo = {
      text: `${trend} vs précédent`,
      color: "text-green-500",
      icon: "↘",
    };
  }

  return { severity, trendInfo, rate, safeWarnings, bypasses };
});

const fetchAiBypass = async () => {
  loadingAiBypass.value = true;
  try {
    const res = await api.get("/admin-api/stats/", {
      params: { period: periodAiBypass.value },
    });
    dataAiBypass.value = res.data.ai_effectiveness;
  } catch (error) {
    console.error("Erreur IA Bypass:", error);
  } finally {
    loadingAiBypass.value = false;
  }
};

// ==============================================
// 3B. Local State: AI Effectiveness (Chart)
// ==============================================
const periodAiChart = ref("total");
const dataAiChart = ref(null);
const loadingAiChart = ref(false);

const fetchAiChart = async () => {
  loadingAiChart.value = true;
  try {
    const res = await api.get("/admin-api/stats/", {
      params: { period: periodAiChart.value },
    });
    dataAiChart.value = res.data.ai_effectiveness;
  } catch (error) {
    console.error("Erreur IA Chart:", error);
  } finally {
    loadingAiChart.value = false;
  }
};
const expandedWaits = ref([]);
const formatAiVerdict = (code) => {
  const map = { BUY: "Acheter", CALM: "Attendre", ABANDON: "Abandonner" };
  return map[code] || code;
};

const calcPercent = (value, total) => {
  if (!total || total === 0) return 0;
  return Math.round((value / total) * 100);
};

const toggleWaitExpanded = (verdict) => {
  const idx = expandedWaits.value.indexOf(verdict);
  if (idx > -1) {
    expandedWaits.value.splice(idx, 1);
  } else {
    expandedWaits.value.push(verdict);
  }
};
// Watchers
watch(periodTotalSaved, fetchTotalSaved);
watch(periodMasteryRatio, fetchMasteryRatio);
watch([periodCategory, topNCategory], fetchCategory);
watch(periodAiBypass, fetchAiBypass);
watch(periodAiChart, fetchAiChart);

// Initialisation
onMounted(() => {
  fetchTotalSaved();
  fetchMasteryRatio();
  fetchCategory();
  fetchAiBypass();
  fetchAiChart();
});
</script>

<style scoped>
/* Utilitaires pour masquer les scrollbars physiquement tout en gardant le scroll fonctionnel */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}

.animate-slide-up {
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
  0% {
    transform: translateY(100%);
  }
  100% {
    transform: translateY(0);
  }
}
</style>
