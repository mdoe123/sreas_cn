(function(Scratch) {
    'use strict';
    class GeoDistanceExtension {
        getInfo() {
            return {
                id: 'geoDistance',
                name: '地理距离计算',
                color1: '#4D7C0F',
                blocks: [
                    {
                        opcode: 'calculateDistance',
                        blockType: Scratch.BlockType.REPORTER,
                        text: '计算纬度[LAT1] 经度[LON1] 到 纬度[LAT2] 经度[LON2] 的距离(米)',
                        arguments: {
                            LAT1: {
                                type: Scratch.ArgumentType.NUMBER,
                                defaultValue: 39.9087 // 北京天安门纬度
                            },
                            LON1: {
                                type: Scratch.ArgumentType.NUMBER,
                                defaultValue: 116.3975 // 北京天安门经度
                            },
                            LAT2: {
                                type: Scratch.ArgumentType.NUMBER,
                                defaultValue: 31.2400 // 上海外滩纬度
                            },
                            LON2: {
                                type: Scratch.ArgumentType.NUMBER,
                                defaultValue: 121.4900 // 上海外滩经度
                            }
                        }
                    }
                ]
            };
        }

        // Haversine公式实现
        calculateDistance(args) {
            const toRadians = (degrees) => degrees * (Math.PI / 180);
            const R = 6371000; // 地球平均半径(米)
            
            const lat1 = toRadians(args.LAT1);
            const lon1 = toRadians(args.LON1);
            const lat2 = toRadians(args.LAT2);
            const lon2 = toRadians(args.LON2);
            
            const dLat = lat2 - lat1;
            const dLon = lon2 - lon1;
            
            const a = 
                Math.sin(dLat / 2) ** 2 + 
                Math.cos(lat1) * Math.cos(lat2) * 
                Math.sin(dLon / 2) ** 2;
                
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
            return Math.round(R * c); // 返回整数距离值
        }
    }

    // 注册扩展
    Scratch.extensions.register(new GeoDistanceExtension());
})(Scratch);