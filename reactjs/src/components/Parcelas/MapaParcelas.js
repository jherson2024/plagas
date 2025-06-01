const MapaParcelas = ({ parcelas }) => {
  const width = 500;
  const height = 400;

  const getX = (lon) => ((lon + 80) * (width / 10));
  const getY = (lat) => ((-lat + 20) * (height / 10));

  return (
    <svg width={width} height={height} style={{ border: '1px solid #ccc', background: '#f9f9f9' }}>
      {parcelas.map((p) => {
        const lat = parseFloat(p.ParLat);
        const lon = parseFloat(p.ParLon);
        if (isNaN(lat) || isNaN(lon)) return null;

        const x = getX(lon);
        const y = getY(lat);

        return (
          <g key={p.ParCod}>
            <circle cx={x} cy={y} r="6" fill="green" />
            <text x={x + 8} y={y} fontSize="10" fill="#333">{p.ParNom}</text>
          </g>
        );
      })}
    </svg>
  );
};

export default MapaParcelas;
3