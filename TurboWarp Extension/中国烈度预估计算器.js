(function(Scratch) {
  'use strict';
  
  class CSISCalculator {
    getInfo() {
      return {
        id: 'csisCalculator',
        name: 'CSIS计算器',
        color1: '#FF8C00',
        color2: '#FF6B00',
        blocks: [
          {
            opcode: 'calculateCSIS',
            blockType: Scratch.BlockType.REPORTER,
            text: '计算中国烈度 震级: [m] 深度: [dep] 距离: [dis]km',
            arguments: {
              m: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 5.0
              },
              dep: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 10.0
              },
              dis: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 100.0
              }
            }
          }
        ]
      };
    }

    calculateCSIS(args) {
      const m = args.m;
      let dep = args.dep;
      const dis = args.dis;
      
      // 输入验证
      if (isNaN(m) || isNaN(dep) || isNaN(dis)) return 0;
      if (dis > 10000) return 0;
      
      // 深度调整
      dep = dep >= 10 ? dep : (Math.max(dep, 0) + 10) / 2;
      
      // 地球半径 (km)
      const r = 6371;
      
      // 计算地心角
      const theta = dis / r;
      
      // 计算直线距离
      const a = r - dep;
      const lineDis = Math.sqrt(a * a + r * r - 2 * a * r * Math.cos(theta));
      
      // 计算校正系数
      const k = 1 - 0.7 / Math.sqrt(dep / 10);
      
      // 计算校正后距离
      const hypoDis = lineDis - k * dep;
      
      // 计算CEA经验公式模型值
      const ceaCsis = 1.297 * m - 4.368 * Math.log10(hypoDis + 8) + 5.363;
      
      // 计算ICL书上给出的经验公式模型值
      const ICLCsis = 1.363 * m - 1.494 * Math.log(hypoDis) + 2.941;
      
      // 返回平均值
      return (ceaCsis + ICLCsis) / 2;
    }
  }
  
  Scratch.extensions.register(new CSISCalculator());
})(Scratch);