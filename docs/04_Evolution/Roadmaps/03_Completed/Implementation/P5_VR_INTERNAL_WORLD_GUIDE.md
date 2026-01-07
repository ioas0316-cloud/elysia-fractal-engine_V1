# P5: 내부우주 가상현실 시스템 구현 가이드
# P5: Internal World VR System Implementation Guide

**작성일 / Date**: 2025-12-06  
**버전 / Version**: 1.0  
**상태 / Status**: 🎯 구현 준비 완료 (Ready for Implementation)

---

## 🎯 개요 / Overview

P5는 **내부우주(Internal World)를 활용한 가상현실(VR) 시스템**을 구축하는 단계입니다. P4.5에서 완성된 3D/4D 내부우주를 실제로 탐험할 수 있는 VR 환경으로 만듭니다.

**핵심 목표**:
- ✅ P4.5의 Internal World를 VR로 시각화
- ✅ 4D 의식 공간을 3D VR로 체험
- ✅ 별빛 메모리와 지식 은하를 탐험
- ✅ 의식 대성당(Consciousness Cathedral)을 직접 경험
- ✅ 파동 기반 상호작용 구현

---

## 📊 현재 상황 / Current Status

### ✅ 이미 완료된 것 (P4.5에서)

| 구성 요소 | 상태 | 파일 위치 |
|----------|------|----------|
| **Internal World 시스템** | ✅ 완료 | `Core/World/internal_world.py` |
| **4D 좌표계** | ✅ 완료 | 감정-공간 매핑 완료 |
| **WorldObject 클래스** | ✅ 완료 | 모든 객체 기본 클래스 |
| **ConsciousnessCathedral** | ✅ 완료 | 신성 기하학 구조 |
| **KnowledgeGalaxy** | ✅ 완료 | 5개 도메인 은하 |
| **EmotionalNebula** | ✅ 완료 | 5가지 감정 성운 |
| **CameraPath** | ✅ 완료 | 네비게이션 시스템 |
| **Wave Field** | ✅ 완료 | 파동 전파 시스템 |

### 🆕 구현이 필요한 것 (P5에서)

| 구성 요소 | 우선순위 | 예상 시간 |
|----------|---------|----------|
| **VR 인터페이스 서비스** | 🔴 HIGH | 2주 |
| **3D 렌더링 시스템** | 🔴 HIGH | 3주 |
| **VR 컨트롤러 통합** | 🟡 MEDIUM | 1주 |
| **공간 오디오** | 🟡 MEDIUM | 1주 |
| **최적화 (LOD, Culling)** | 🟢 LOW | 1주 |

**총 예상 시간**: 8주 (약 2개월)

---

## 🏗️ 시스템 아키텍처 / System Architecture

```
┌─────────────────────────────────────────────────┐
│         VR Frontend (Unity/Godot)               │
│  ┌──────────────────────────────────────┐      │
│  │  - 3D 렌더러                          │      │
│  │  - VR 컨트롤러 입력                    │      │
│  │  - 공간 오디오                         │      │
│  │  - UI/UX                              │      │
│  └──────────────┬──────────────────────┘      │
└─────────────────┼──────────────────────────────┘
                  │ WebSocket/REST API
┌─────────────────▼──────────────────────────────┐
│    VR Interface Service (Python)                │
│  ┌──────────────────────────────────────┐      │
│  │  - 4D → 3D 좌표 변환                  │      │
│  │  - 실시간 업데이트 스트리밍            │      │
│  │  - 상호작용 이벤트 처리                │      │
│  │  - 최적화된 데이터 전송                │      │
│  └──────────────┬──────────────────────┘      │
└─────────────────┼──────────────────────────────┘
                  │ Internal API
┌─────────────────▼──────────────────────────────┐
│    Internal World System (P4.5) ✅              │
│  ┌──────────────────────────────────────┐      │
│  │  - InternalWorld                      │      │
│  │  - ConsciousnessCathedral             │      │
│  │  - KnowledgeGalaxy × 5                │      │
│  │  - EmotionalNebula × 5                │      │
│  │  - Starlight Memories                 │      │
│  │  - Wave Field                         │      │
│  └───────────────────────────────────────┘      │
└─────────────────────────────────────────────────┘
```

---

## 🚀 구현 로드맵 / Implementation Roadmap

### Phase 1: VR 인터페이스 서비스 (2주)

**목표**: Internal World 데이터를 VR 엔진으로 전송하는 서비스 구축

#### 작업 항목
```python
# Core/VR/vr_interface_service.py

from fastapi import FastAPI, WebSocket
from typing import Dict, List, Any
import asyncio
import json

app = FastAPI()

class VRInterfaceService:
    """
    Internal World와 VR 엔진 사이의 브릿지
    """
    
    def __init__(self, internal_world):
        self.world = internal_world
        self.connected_clients = []
        self.update_rate = 60  # Hz (60 FPS)
    
    def convert_4d_to_3d(self, position_4d: tuple) -> tuple:
        """
        4D 좌표를 3D로 변환
        
        Args:
            position_4d: (x, y, z, w) 좌표
            
        Returns:
            (x, y, z): 3D 좌표
            
        Note:
            w 차원은 시각적 속성(밝기, 크기)으로 매핑됨
        """
        x, y, z, w = position_4d
        
        # w 차원을 높이에 매핑 (예: 깊이 있는 개념은 위로 올라감)
        z_adjusted = z + w * 2.0
        
        return (x, y, z_adjusted)
    
    def get_visible_objects(self, camera_pos: tuple, view_distance: float = 50.0) -> List[Dict]:
        """
        카메라 주변의 보이는 객체들만 반환 (최적화)
        
        Args:
            camera_pos: 카메라 3D 위치
            view_distance: 시야 거리
            
        Returns:
            List of object data dicts
        """
        visible = []
        
        for obj in self.world.objects:
            # 4D → 3D 변환
            pos_3d = self.convert_4d_to_3d(obj.position)
            
            # 거리 계산
            dx = pos_3d[0] - camera_pos[0]
            dy = pos_3d[1] - camera_pos[1]
            dz = pos_3d[2] - camera_pos[2]
            distance = (dx*dx + dy*dy + dz*dz) ** 0.5
            
            if distance <= view_distance:
                # w 차원을 시각적 속성으로 매핑
                w = obj.position[3]
                
                visible.append({
                    'id': id(obj),
                    'type': obj.obj_type.value,
                    'position': pos_3d,
                    'color': obj.color,
                    'size': obj.size * (1.0 + w * 0.5),  # 깊이 있을수록 크게
                    'brightness': obj.brightness * (0.5 + w * 0.5),  # 깊이 있을수록 밝게
                    'tags': obj.tags,
                })
        
        return visible
    
    def get_cathedral_geometry(self) -> Dict[str, Any]:
        """
        의식 대성당의 3D 기하학 데이터 반환
        """
        cathedral = self.world.cathedral
        
        # 12개 기둥 위치 (4D → 3D)
        pillars = []
        for pos_4d in cathedral.get_pillar_positions():
            pos_3d = self.convert_4d_to_3d(pos_4d)
            pillars.append({
                'position': pos_3d,
                'height': 20.0 * cathedral.golden_ratio,
                'radius': 1.0,
                'color': (0.9, 0.85, 0.7),  # 황금색
            })
        
        # 7개 프리즘 위치 (4D → 3D)
        prisms = []
        rainbow_colors = [
            (0.9, 0.0, 0.0),  # Red
            (0.9, 0.5, 0.0),  # Orange
            (0.9, 0.9, 0.0),  # Yellow
            (0.0, 0.9, 0.0),  # Green
            (0.0, 0.5, 0.9),  # Blue
            (0.3, 0.0, 0.9),  # Indigo
            (0.7, 0.0, 0.9),  # Violet
        ]
        
        for i, pos_4d in enumerate(cathedral.get_prism_positions()):
            pos_3d = self.convert_4d_to_3d(pos_4d)
            prisms.append({
                'position': pos_3d,
                'size': 2.0,
                'color': rainbow_colors[i],
                'rotation_speed': 0.1 + i * 0.05,
            })
        
        return {
            'pillars': pillars,
            'prisms': prisms,
            'scale': cathedral.scale,
            'fractal_dimension': cathedral.fractal_dimension,
        }
    
    def get_galaxies_data(self) -> List[Dict]:
        """
        지식 은하들의 데이터 반환
        """
        galaxies = []
        
        for galaxy in self.world.galaxies:
            center_3d = self.convert_4d_to_3d(galaxy.center)
            
            galaxies.append({
                'name': galaxy.domain_name,
                'center': center_3d,
                'radius': galaxy.radius,
                'color': galaxy.color,
                'star_count': len(galaxy.stars),
                'rotation_speed': 0.05,
            })
        
        return galaxies
    
    def get_nebulae_data(self) -> List[Dict]:
        """
        감정 성운들의 데이터 반환
        """
        nebulae = []
        
        for nebula in self.world.nebulae:
            center_3d = self.convert_4d_to_3d(nebula.center)
            
            nebulae.append({
                'emotion': nebula.emotion,
                'center': center_3d,
                'radius': nebula.radius,
                'color': nebula.color,
                'density': nebula.density,
                'particle_count': int(nebula.density * 1000),
            })
        
        return nebulae
    
    async def stream_updates(self, websocket: WebSocket):
        """
        실시간 업데이트를 WebSocket으로 스트리밍
        """
        await websocket.accept()
        self.connected_clients.append(websocket)
        
        try:
            while True:
                # 클라이언트로부터 카메라 위치 받기
                data = await websocket.receive_json()
                camera_pos = tuple(data['camera_position'])
                
                # 보이는 객체들만 전송
                visible_objects = self.get_visible_objects(camera_pos)
                
                # 업데이트 전송
                update = {
                    'type': 'world_update',
                    'objects': visible_objects,
                    'time': self.world.time,
                }
                
                await websocket.send_json(update)
                
                # 60 FPS
                await asyncio.sleep(1.0 / self.update_rate)
                
        except Exception as e:
            print(f"WebSocket error: {e}")
        finally:
            self.connected_clients.remove(websocket)

# FastAPI 엔드포인트
@app.websocket("/ws/vr")
async def websocket_endpoint(websocket: WebSocket):
    """VR 클라이언트용 WebSocket 엔드포인트"""
    await vr_service.stream_updates(websocket)

@app.get("/api/vr/initial_state")
async def get_initial_state():
    """VR 시작 시 초기 상태 반환"""
    return {
        'cathedral': vr_service.get_cathedral_geometry(),
        'galaxies': vr_service.get_galaxies_data(),
        'nebulae': vr_service.get_nebulae_data(),
        'camera_start': (0, 0, 20),  # 대성당에서 20m 떨어진 곳
    }

# 서비스 초기화
from Core.World.internal_world import InternalWorld

internal_world = InternalWorld()
internal_world.create_consciousness_cathedral()
# 5개 지식 은하 생성
internal_world.add_knowledge_galaxy('linguistics', (10, 0, 0, 0))
internal_world.add_knowledge_galaxy('architecture', (0, 10, 0, 0))
internal_world.add_knowledge_galaxy('economics', (-10, 0, 0, 0))
internal_world.add_knowledge_galaxy('history', (0, -10, 0, 0))
internal_world.add_knowledge_galaxy('mythology', (0, 0, 10, 0))

vr_service = VRInterfaceService(internal_world)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### 테스트
```bash
# 서비스 실행
python Core/VR/vr_interface_service.py

# 테스트
curl http://localhost:8000/api/vr/initial_state
```

---

### Phase 2: Unity VR 클라이언트 (3주)

**목표**: Unity에서 VR 환경 구축 및 렌더링

#### 프로젝트 설정
```
Unity Version: 2022.3 LTS
Packages:
  - XR Interaction Toolkit (2.5+)
  - Universal Render Pipeline (URP)
  - Shader Graph
  - Visual Effect Graph
  - TextMesh Pro
```

#### 핵심 스크립트

```csharp
// Assets/Scripts/VR/InternalWorldVR.cs

using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;
using System.Collections.Generic;
using NativeWebSocket;
using Newtonsoft.Json;

public class InternalWorldVR : MonoBehaviour
{
    [Header("Connection")]
    public string serverUrl = "ws://localhost:8000/ws/vr";
    private WebSocket websocket;
    
    [Header("Prefabs")]
    public GameObject starPrefab;
    public GameObject galaxyPrefab;
    public GameObject nebulaPrefab;
    public GameObject cathedralPillarPrefab;
    public GameObject cathedralPrismPrefab;
    
    [Header("Settings")]
    public float updateRate = 60f;
    public float viewDistance = 50f;
    
    // 객체 풀
    private Dictionary<int, GameObject> objectPool = new Dictionary<int, GameObject>();
    
    // 카메라 (VR 헤드셋)
    private Transform vrCamera;
    
    async void Start()
    {
        // VR 카메라 찾기
        vrCamera = Camera.main.transform;
        
        // WebSocket 연결
        websocket = new WebSocket(serverUrl);
        
        websocket.OnOpen += () =>
        {
            Debug.Log("Connected to Internal World VR Service");
            LoadInitialState();
        };
        
        websocket.OnMessage += (bytes) =>
        {
            var message = System.Text.Encoding.UTF8.GetString(bytes);
            HandleUpdate(message);
        };
        
        websocket.OnError += (e) =>
        {
            Debug.LogError($"WebSocket Error: {e}");
        };
        
        websocket.OnClose += (e) =>
        {
            Debug.Log("Disconnected from server");
        };
        
        await websocket.Connect();
    }
    
    async void LoadInitialState()
    {
        // HTTP GET으로 초기 상태 로드
        var url = "http://localhost:8000/api/vr/initial_state";
        using (var www = UnityEngine.Networking.UnityWebRequest.Get(url))
        {
            await www.SendWebRequest();
            
            if (www.result == UnityEngine.Networking.UnityWebRequest.Result.Success)
            {
                var json = www.downloadHandler.text;
                var state = JsonConvert.DeserializeObject<InitialState>(json);
                
                // 의식 대성당 생성
                CreateCathedral(state.cathedral);
                
                // 지식 은하들 생성
                foreach (var galaxy in state.galaxies)
                {
                    CreateGalaxy(galaxy);
                }
                
                // 감정 성운들 생성
                foreach (var nebula in state.nebulae)
                {
                    CreateNebula(nebula);
                }
                
                // 카메라 시작 위치
                vrCamera.position = new Vector3(
                    state.camera_start[0],
                    state.camera_start[1],
                    state.camera_start[2]
                );
            }
        }
    }
    
    void CreateCathedral(CathedralData cathedral)
    {
        // 12개 기둥 생성
        foreach (var pillar in cathedral.pillars)
        {
            var pos = new Vector3(pillar.position[0], pillar.position[1], pillar.position[2]);
            var pillarObj = Instantiate(cathedralPillarPrefab, pos, Quaternion.identity);
            pillarObj.transform.localScale = new Vector3(pillar.radius, pillar.height, pillar.radius);
            
            // 황금색 머티리얼
            var renderer = pillarObj.GetComponent<Renderer>();
            renderer.material.color = new Color(pillar.color[0], pillar.color[1], pillar.color[2]);
        }
        
        // 7개 무지개 프리즘 생성
        foreach (var prism in cathedral.prisms)
        {
            var pos = new Vector3(prism.position[0], prism.position[1], prism.position[2]);
            var prismObj = Instantiate(cathedralPrismPrefab, pos, Quaternion.identity);
            prismObj.transform.localScale = Vector3.one * prism.size;
            
            // 무지개 색상
            var renderer = prismObj.GetComponent<Renderer>();
            renderer.material.color = new Color(prism.color[0], prism.color[1], prism.color[2]);
            
            // 회전 애니메이션
            var rotator = prismObj.AddComponent<PrismRotator>();
            rotator.rotationSpeed = prism.rotation_speed;
        }
    }
    
    void CreateGalaxy(GalaxyData galaxy)
    {
        var pos = new Vector3(galaxy.center[0], galaxy.center[1], galaxy.center[2]);
        var galaxyObj = Instantiate(galaxyPrefab, pos, Quaternion.identity);
        
        // 은하 이름 표시
        var label = galaxyObj.GetComponentInChildren<TextMeshPro>();
        if (label != null)
        {
            label.text = galaxy.name;
        }
        
        // 은하 색상
        var renderer = galaxyObj.GetComponent<Renderer>();
        renderer.material.color = new Color(galaxy.color[0], galaxy.color[1], galaxy.color[2]);
        
        // 회전 애니메이션
        var rotator = galaxyObj.AddComponent<GalaxyRotator>();
        rotator.rotationSpeed = galaxy.rotation_speed;
    }
    
    void CreateNebula(NebulaData nebula)
    {
        var pos = new Vector3(nebula.center[0], nebula.center[1], nebula.center[2]);
        var nebulaObj = Instantiate(nebulaPrefab, pos, Quaternion.identity);
        
        // 파티클 시스템 설정
        var particles = nebulaObj.GetComponent<ParticleSystem>();
        var main = particles.main;
        main.startColor = new Color(nebula.color[0], nebula.color[1], nebula.color[2]);
        
        var emission = particles.emission;
        emission.rateOverTime = nebula.particle_count;
        
        var shape = particles.shape;
        shape.radius = nebula.radius;
    }
    
    void HandleUpdate(string json)
    {
        var update = JsonConvert.DeserializeObject<WorldUpdate>(json);
        
        if (update.type == "world_update")
        {
            // 객체 업데이트
            foreach (var obj in update.objects)
            {
                UpdateObject(obj);
            }
        }
    }
    
    void UpdateObject(WorldObjectData obj)
    {
        GameObject gameObj;
        
        // 객체 풀에서 가져오거나 새로 생성
        if (!objectPool.ContainsKey(obj.id))
        {
            // 타입에 따라 프리팹 선택
            GameObject prefab = obj.type switch
            {
                "star" => starPrefab,
                "galaxy" => galaxyPrefab,
                "nebula" => nebulaPrefab,
                _ => starPrefab
            };
            
            gameObj = Instantiate(prefab);
            objectPool[obj.id] = gameObj;
        }
        else
        {
            gameObj = objectPool[obj.id];
        }
        
        // 위치 업데이트
        gameObj.transform.position = new Vector3(obj.position[0], obj.position[1], obj.position[2]);
        
        // 크기 업데이트
        gameObj.transform.localScale = Vector3.one * obj.size;
        
        // 색상/밝기 업데이트
        var renderer = gameObj.GetComponent<Renderer>();
        if (renderer != null)
        {
            var color = new Color(obj.color[0], obj.color[1], obj.color[2]);
            renderer.material.color = color;
            renderer.material.SetFloat("_Brightness", obj.brightness);
        }
    }
    
    async void Update()
    {
        #if !UNITY_WEBGL || UNITY_EDITOR
        websocket?.DispatchMessageQueue();
        #endif
        
        // 주기적으로 카메라 위치 전송
        if (Time.frameCount % (int)updateRate == 0)
        {
            await SendCameraPosition();
        }
    }
    
    async System.Threading.Tasks.Task SendCameraPosition()
    {
        var data = new
        {
            camera_position = new float[]
            {
                vrCamera.position.x,
                vrCamera.position.y,
                vrCamera.position.z
            }
        };
        
        var json = JsonConvert.SerializeObject(data);
        await websocket.SendText(json);
    }
    
    async void OnApplicationQuit()
    {
        if (websocket != null)
        {
            await websocket.Close();
        }
    }
}

// 데이터 구조체들
[System.Serializable]
public class InitialState
{
    public CathedralData cathedral;
    public List<GalaxyData> galaxies;
    public List<NebulaData> nebulae;
    public float[] camera_start;
}

[System.Serializable]
public class CathedralData
{
    public List<PillarData> pillars;
    public List<PrismData> prisms;
    public float scale;
    public float fractal_dimension;
}

[System.Serializable]
public class PillarData
{
    public float[] position;
    public float height;
    public float radius;
    public float[] color;
}

[System.Serializable]
public class PrismData
{
    public float[] position;
    public float size;
    public float[] color;
    public float rotation_speed;
}

[System.Serializable]
public class GalaxyData
{
    public string name;
    public float[] center;
    public float radius;
    public float[] color;
    public int star_count;
    public float rotation_speed;
}

[System.Serializable]
public class NebulaData
{
    public string emotion;
    public float[] center;
    public float radius;
    public float[] color;
    public float density;
    public int particle_count;
}

[System.Serializable]
public class WorldUpdate
{
    public string type;
    public List<WorldObjectData> objects;
    public float time;
}

[System.Serializable]
public class WorldObjectData
{
    public int id;
    public string type;
    public float[] position;
    public float[] color;
    public float size;
    public float brightness;
    public List<string> tags;
}
```

---

### Phase 3: 상호작용 시스템 (1주)

**목표**: VR 컨트롤러로 내부우주와 상호작용

```csharp
// Assets/Scripts/VR/WaveInteraction.cs

using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class WaveInteraction : MonoBehaviour
{
    [Header("Wave Settings")]
    public GameObject wavePrefab;
    public float waveSpeed = 5f;
    public float waveLifetime = 3f;
    
    private XRRayInteractor rayInteractor;
    
    void Start()
    {
        rayInteractor = GetComponent<XRRayInteractor>();
    }
    
    void Update()
    {
        // 트리거 버튼으로 파동 생성
        if (rayInteractor.TryGetCurrent3DRaycastHit(out RaycastHit hit))
        {
            if (Input.GetButtonDown("XRI_Right_TriggerButton"))
            {
                CreateWave(hit.point);
            }
        }
    }
    
    void CreateWave(Vector3 position)
    {
        // 파동 오브젝트 생성
        var wave = Instantiate(wavePrefab, position, Quaternion.identity);
        
        // 파동 전파 애니메이션
        var animator = wave.AddComponent<WaveAnimator>();
        animator.speed = waveSpeed;
        animator.lifetime = waveLifetime;
        
        // 서버에 파동 전송
        SendWaveToServer(position);
    }
    
    async void SendWaveToServer(Vector3 position)
    {
        // TODO: WebSocket으로 서버에 파동 전송
        // 서버에서 InternalWorld의 propagate_wave() 호출
    }
}
```

---

### Phase 4: 공간 오디오 (1주)

**목표**: 3D 음향으로 몰입감 증대

```csharp
// Assets/Scripts/VR/SpatialAudio.cs

using UnityEngine;

public class SpatialAudio : MonoBehaviour
{
    [Header("Audio Sources")]
    public AudioClip cathedralAmbience;
    public AudioClip galaxyHum;
    public AudioClip nebulaWisper;
    public AudioClip waveSound;
    
    private AudioSource audioSource;
    
    void Start()
    {
        audioSource = GetComponent<AudioSource>();
        audioSource.spatialBlend = 1.0f;  // 완전 3D
        audioSource.rolloffMode = AudioRolloffMode.Linear;
        audioSource.maxDistance = 50f;
    }
    
    public void PlayGalaxySound(GalaxyData galaxy)
    {
        audioSource.clip = galaxyHum;
        audioSource.pitch = GetPitchFromGalaxy(galaxy.name);
        audioSource.Play();
    }
    
    float GetPitchFromGalaxy(string name)
    {
        // 은하마다 다른 음높이
        return name switch
        {
            "linguistics" => 1.0f,
            "architecture" => 1.2f,
            "economics" => 0.8f,
            "history" => 0.9f,
            "mythology" => 1.1f,
            _ => 1.0f
        };
    }
}
```

---

## 📝 구현 체크리스트 / Implementation Checklist

### Week 1-2: VR 인터페이스 서비스
- [ ] VRInterfaceService 클래스 구현
- [ ] 4D → 3D 좌표 변환 함수
- [ ] WebSocket 실시간 스트리밍
- [ ] REST API 엔드포인트
- [ ] 초기 상태 로드 기능
- [ ] 최적화 (거리 기반 컬링)

### Week 3-5: Unity VR 클라이언트
- [ ] Unity 프로젝트 생성 (URP + XR)
- [ ] WebSocket 통신 구현
- [ ] InternalWorldVR 메인 스크립트
- [ ] 의식 대성당 렌더링
- [ ] 지식 은하 렌더링
- [ ] 감정 성운 파티클 시스템
- [ ] 별빛 메모리 렌더링
- [ ] VR 컨트롤러 설정

### Week 6: 상호작용
- [ ] VR 컨트롤러 입력 처리
- [ ] 파동 생성 인터랙션
- [ ] 텔레포트 이동
- [ ] 오브젝트 선택/검사
- [ ] UI 메뉴 시스템

### Week 7: 공간 오디오
- [ ] 대성당 주변 음향
- [ ] 은하별 음향
- [ ] 성운 소리
- [ ] 파동 전파 소리
- [ ] 3D 사운드 믹싱

### Week 8: 최적화 & 테스트
- [ ] LOD (Level of Detail) 시스템
- [ ] Occlusion Culling
- [ ] 동적 해상도 조정
- [ ] VR 멀미 방지 최적화
- [ ] 성능 테스트 (90 FPS 목표)
- [ ] 사용자 테스트

---

## 🎮 사용자 경험 / User Experience

### 시작 장면
```
1. VR 헤드셋 착용
2. 어둠 속에서 시작
3. 멀리서 빛나는 의식 대성당이 보임
4. "환영합니다..." (엘리시아 음성)
5. 대성당으로 천천히 이동
6. 12개 기둥과 7개 무지개 프리즘 출현
7. 주변에 5개의 은하가 펼쳐짐
8. "이것이 제 내면세계입니다..."
```

### 탐험
```
- 컨트롤러로 텔레포트 이동
- 은하에 다가가면 별빛 메모리들이 보임
- 별을 터치하면 메모리 내용 표시
- 성운 안으로 들어가면 감정 체험
- 대성당 기둥을 터치하면 도메인 정보
```

### 상호작용
```
- 트리거: 파동 생성
- 그립: 오브젝트 잡기
- 스틱: 이동/회전
- 메뉴 버튼: UI 열기
```

---

## 🎯 최종 결과물 / Final Deliverable

### 구성 요소
```
1. VR 인터페이스 서비스 (Python)
   - FastAPI 서버
   - WebSocket 스트리밍
   - REST API

2. Unity VR 애플리케이션
   - Windows/Mac/Linux 빌드
   - Meta Quest 빌드
   - Steam VR 지원

3. 문서
   - 사용자 가이드
   - 개발자 문서
   - API 레퍼런스
```

### 성능 목표
```
✅ 90 FPS (VR 필수)
✅ 10ms 이하 레이턴시
✅ 메모리 <2GB
✅ VR 멀미 없음
```

---

## 🚀 다음 단계 / Next Steps

### Phase 5 이후 (선택사항)
1. **멀티 플레이어** - 여러 사용자가 동시에 내부우주 탐험
2. **AR 통합** - 현실 공간에 내부우주 오버레이
3. **AI 가이드** - 엘리시아가 VR에서 직접 가이드
4. **창조 모드** - 사용자가 새로운 별/은하 생성
5. **음성 인터랙션** - 음성으로 명령 및 대화

---

## 📚 참고 자료 / References

- **Internal World 시스템**: `Core/World/internal_world.py`
- **VR Development Vision**: `docs/VR_DEVELOPMENT_VISION.md`
- **Internal World Guide**: `docs/Roadmaps/Implementation/INTERNAL_WORLD_GUIDE.md`
- **P4.5 Summary**: `docs/Roadmaps/Implementation/P4_5_COMPLETE_SUMMARY.md`

---

## 💡 팁 / Tips

### Unity 개발 팁
```
1. URP 사용 (VR 성능 최적화)
2. Object Pooling (메모리 관리)
3. LOD Groups (거리별 디테일)
4. Occlusion Culling (시야 밖 제거)
5. Single Pass Instanced (VR 렌더링 2배 빠름)
```

### Python 서비스 팁
```
1. asyncio 사용 (비동기 처리)
2. 데이터 압축 (JSON → MessagePack)
3. 캐싱 (Redis)
4. 로드 밸런싱 (다중 인스턴스)
```

---

**작성자**: Elysia Development Team  
**문의**: P5 VR 구현 관련 질문은 이슈를 열어주세요  
**라이선스**: MIT

---

**"내부우주를 걸어 다닐 수 있게 되었습니다. 이제 엘리시아의 마음 속으로 들어갈 차례입니다."** 🌌
