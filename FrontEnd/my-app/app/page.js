'use client'
import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';

const ApexCharts = dynamic(() => import('react-apexcharts'), { ssr: false });

const GenderChart = () => {
  const [categories, setCategories] = useState([]);
  const [series, setSeries] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const response = await fetch('https://user-data-2024.s3.amazonaws.com/user-data-2024.json');
      const data = await response.json();

      // Extract categories and series data
      const categories = Object.keys(data);
      const series = Object.values(data);

      setCategories(categories);
      setSeries([{ name: 'Gender Count', data: series }]);
    }

    fetchData();
  }, []);

  const chartOptions = {
    chart: {
      type: 'bar'
    },
    xaxis: {
      categories: categories
    }
  };
  return (
    <div className='flex gap-2'>
      <ApexCharts options={chartOptions} series={series} type="bar" width={800} height={300} />
    </div>
  );
};

export default GenderChart;

