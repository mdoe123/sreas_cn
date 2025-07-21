import requests
import json
import time

def get_all_china_cities_and_districts(api_key):
    """
    获取中国所有市级行政区划（包括直辖市下属区）名称及中心经纬度
    :param api_key: 高德地图API密钥
    :return: 行政区划列表，格式[{'name': '北京市', 'center': '116.407394,39.904211'}, ...]
    """
    #获取所有省级行政区
    base_url = "https://restapi.amap.com/v3/config/district"
    params = {
        "key": api_key,
        "keywords": "中国",
        "subdistrict": "1",
        "extensions": "base"
    }

    # 获取省级数据
    response = requests.get(base_url, params=params)
    time.sleep(1)  # 添加1秒时间间隔
    province_data = response.json()

    if province_data["status"] != "1":
        print(f"获取省级数据失败: {province_data.get('info', '未知错误')}")
        return []

    # 存储所有行政区划
    all_areas = []

    # 直辖市列表
    municipalities = ["北京市", "天津市", "上海市", "重庆市"]

    #遍历每个省份获取下属行政区
    for province in province_data["districts"][0]["districts"]:
        # 处理直辖市及其下属区
        if province["name"] in municipalities:
            # 添加直辖市本身
            all_areas.append({
                "name": province["name"],
                "center": province["center"],
                "level": "province"
            })
            print(f"添加直辖市: {province['name']}")

            # 获取该直辖市下属区级行政区
            district_params = {
                "key": api_key,
                "keywords": province["adcode"],
                "subdistrict": "2",  # 获取到区县级
                "extensions": "base"
            }

            district_response = requests.get(base_url, params=district_params)
            time.sleep(1)  # 添加1秒时间间隔
            district_data = district_response.json()

            if district_data["status"] != "1":
                print(f"获取{province['name']}区县数据失败: {district_data.get('info', '未知错误')}")
                continue

            # 提取区级行政区
            for district in district_data["districts"][0]["districts"]:
                if district["level"] == "district":
                    all_areas.append({
                        "name": district["name"],
                        "center": district["center"],
                        "level": "district"
                    })
                    print(f"  └─ 添加区: {district['name']}")
        else:
            # 处理普通省份下属市级行政区
            city_params = {
                "key": api_key,
                "keywords": province["adcode"],
                "subdistrict": "2",  # 获取到县级
                "extensions": "base"
            }

            city_response = requests.get(base_url, params=city_params)
            time.sleep(1)  # 添加时间间隔
            city_data = city_response.json()

            if city_data["status"] != "1":
                print(f"获取{province['name']}城市数据失败: {city_data.get('info', '未知错误')}")
                continue

            # 提取市级行政区
            for city in city_data["districts"][0]["districts"]:
                # 只处理市级单位（包括地级市、自治州等）
                if city["level"] in ["city", "province"]:
                    all_areas.append({
                        "name": city["name"],
                        "center": city["center"],
                        "level": "city"
                    })
                    print(f"添加城市: {city['name']}")

    return all_areas

# 高德地图API密钥
API_KEY = ""

# 获取所有行政区数据
areas = get_all_china_cities_and_districts(API_KEY)

# 分类
cities = [a for a in areas if a["level"] == "city"]
districts = [a for a in areas if a["level"] == "district"]
provinces = [a for a in areas if a["level"] == "province"]

# 打印结果
print(f"\n统计结果:")
print(f"- 省级直辖市: {len(provinces)} 个")
print(f"- 地级市: {len(cities)} 个")
print(f"- 直辖市下属区: {len(districts)} 个")
print(f"总计: {len(areas)} 个行政区划")

# 保存到JSON
with open('china_administrative_areas.json', 'w', encoding='utf-8') as f:
    json.dump(areas, f, ensure_ascii=False, indent=2)
    print("\n数据已保存到 china_administrative_areas.json")
