$(document).ready(function() {
	// Area chart
	if ($('#stud_gender').length > 0) {
	var options = {
		chart: {
			height: 350,
			type: "area",
			toolbar: {
				show: false
			},
		},
		dataLabels: {
			enabled: false
		},
		stroke: {
			curve: "smooth"
		},
		series: [{
			name: "Teachers",
			data: [45, 60, 75, 51, 42, 42, 30]
		}, {
			name: "Students",
			color: '#FFBC13',
			data: [24, 48, 56, 32, 34, 52, 25]
		}],
		xaxis: {
			categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
		}
	}
	var chart = new ApexCharts(
		document.querySelector("#apexcharts-area"),
		options
	);
	chart.render();
	}

	// Bar chart

	if ($('#stud_gender').length > 0) {
	var optionsBar = {
		chart: {
			type: 'bar',
			height: 350,
			width: '100%',
			stacked: true,
			toolbar: {
				show: false
			},
		},
		dataLabels: {
			enabled: false
		},
		plotOptions: {
			bar: {
				columnWidth: '45%',
			}
		},
		series: [{
			name: "Boys",
			color: '#fdbb38',
			data: [{{staff_female}}],
		}, {
			name: "Girls",
			color: '#19affb',
			data: [{{staff_female}}],
		}],
		labels: [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
		xaxis: {
			labels: {
				show: false
			},
			axisBorder: {
				show: false
			},
			axisTicks: {
				show: false
			},
		},
		yaxis: {
			axisBorder: {
				show: false
			},
			axisTicks: {
				show: false
			},
			labels: {
				style: {
					colors: '#777'
				}
			}
		},
		title: {
			text: '',
			align: 'left',
			style: {
				fontSize: '18px'
			}
		}

	}

	var chartBar = new ApexCharts(document.querySelector('#stud_gender'), optionsBar);
	chartBar.render();
	}

	// Bar chart

	if ($('#char_task').length > 0) {
	var optionsPie = {
		chart: {
			width: '100%',
			height: 397,
			type: 'pie',
		},
		labels: ['Отложенные', 'В процессе', 'На доработоку', 'Завершенные'],
		series: [{{deferred_count}}, {{in_progress_count}}, {{needs_rework_count}}, {{completed_count}}],
		plotOptions: {
			pie: {
				donut: {
					size: '65%'
				}
			}
		},
		legend: {
			position: 'bottom'
		},
	};
	var chartPie = new ApexCharts(document.querySelector('#char_task'), optionsPie);
	chartPie.render();
    }

    // Bar chart

	if ($('#char').length > 0) {
	var optionsPie = {
		chart: {
			width: '100%',
			height: 397,
			type: 'pie',
		},
		labels: ['В процессе', 'На доработоку', 'Отложенные', 'Завершенные', 'Новые','В ожидании'],
		series: [{{in_progress_count}}, {{needs_rework_count}}, {{deferred_count}}, {{completed_count}}, {{newTask}}, {{waitingTask}}],
		plotOptions: {
			pie: {
				donut: {
					size: '65%'
				}
			}
		},
		legend: {
			position: 'bottom'
		},
	};
	var chartPie = new ApexCharts(document.querySelector('#char'), optionsPie);
	chartPie.render();
    }

    if ($('#char_task_ana').length > 0) {
	var optionsPie = {
		chart: {
			width: '100%',
			height: 397,
			type: 'pie',
		},
		labels: ['Почти просрочены', 'Не просмотренная', 'Просроченная'],
		series: [{{task_almost_overdue}}, {{unreviewed_task}}, {{overdue_task}}],
		plotOptions: {
			pie: {
				donut: {
					size: '65%'
				}
			}
		},
		legend: {
			position: 'bottom'
		},
	};
	var chartPie = new ApexCharts(document.querySelector('#char_task_ana'), optionsPie);
	chartPie.render();
    }

    // Bar chart

	if ($('#char_call').length > 0) {
	var optionsPie = {
		chart: {
			width: '100%',
			height: 397,
			type: 'pie',
		},
		labels: ['Звонки больше 5 минут', 'Звонки меньше 30 секунд'],
		series: [{{number_calls_more_5}}, {{number_calls_less_30}}],
		plotOptions: {
			pie: {
				donut: {
					size: '65%'
				}
			}
		},
		legend: {
			position: 'bottom'
		},
	};
	var chartPie = new ApexCharts(document.querySelector('#char_call'), optionsPie);
	chartPie.render();
    }

    // Bar chart

	if ($('#char_din_call').length > 0) {
	var optionsBar = {
		chart: {
			type: 'bar',
			height: 350,
			width: '100%',
			stacked: true,
			toolbar: {
				show: false
			},
		},
		dataLabels: {
			enabled: false
		},
		plotOptions: {
			bar: {
				columnWidth: '45%',
			}
		},
		series: [
		{
			name: "Исходящие",
			color: '#FF5733',
			data: [{{total_Incoming_calls}}],
		},
		{
			name: "Входящие",
			color: '#3366FF',
			data: [{{total_outgoing_calls}}],
		}
		],
		labels: ['Звонки'],
		xaxis: {
			labels: {
				show: false
			},
			axisBorder: {
				show: false
			},
			axisTicks: {
				show: false
			},
		},
		yaxis: {
			axisBorder: {
				show: false
			},
			axisTicks: {
				show: false
			},
			labels: {
				style: {
					colors: '#777'
				}
			}
		},
		title: {
			text: '',
			align: 'left',
			style: {
				fontSize: '18px'
			}
		}
	}
	var chartBar = new ApexCharts(document.querySelector('#char_din_call'), optionsBar);
	chartBar.render();
	}
	if ($('#char_type').length > 0) {
	var optionsBar = {
		chart: {
			type: 'bar',
			height: 350,
			width: '100%',
			stacked: true,
			toolbar: {
				show: false
			},
		},
		dataLabels: {
			enabled: false
		},
		plotOptions: {
			bar: {
				columnWidth: '45%',
			}
		},
		series: [
		{
            name: "Пропущенные",
            color: '#FF5733',
            data: [{{total_missed_calls}}],
        },
        {
            name: "Отклоненные",
            color: '#3366FF',
            data: [{{rejected_calls}}],
        },
        {
            name: "Занятые",
            color: '#33FF33',
            data: [{{busy_calls}}],
        }
		],
		labels: ['Звонки'],
		xaxis: {
			labels: {
				show: false
			},
			axisBorder: {
				show: false
			},
			axisTicks: {
				show: false
			},
		},
		yaxis: {
			axisBorder: {
				show: false
			},
			axisTicks: {
				show: false
			},
			labels: {
				style: {
					colors: '#777'
				}
			}
		},
		title: {
			text: '',
			align: 'left',
			style: {
				fontSize: '18px'
			}
		}
	}
	var chartBar = new ApexCharts(document.querySelector('#char_type'), optionsBar);
	chartBar.render();
	}
});