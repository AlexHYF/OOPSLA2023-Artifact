
(set-logic BV)

(define-fun shr1 ((x (BitVec 64))) (BitVec 64) (bvlshr x #x0000000000000001))
(define-fun shr4 ((x (BitVec 64))) (BitVec 64) (bvlshr x #x0000000000000004))
(define-fun shr16 ((x (BitVec 64))) (BitVec 64) (bvlshr x #x0000000000000010))
(define-fun shl1 ((x (BitVec 64))) (BitVec 64) (bvshl x #x0000000000000001))
(define-fun if0 ((x (BitVec 64)) (y (BitVec 64)) (z (BitVec 64))) (BitVec 64) (ite (= x #x0000000000000001) y z))

(synth-fun f ( (x (BitVec 64))) (BitVec 64)
(

(Start (BitVec 64) (#x0000000000000000 #x0000000000000001 x (bvnot Start)
                    (shl1 Start)
 		    (shr1 Start)
		    (shr4 Start)
		    (shr16 Start)
		    (bvand Start Start)
		    (bvor Start Start)
		    (bvxor Start Start)
		    (bvadd Start Start)
		    (if0 Start Start Start)
 ))
)
)


(constraint (= (f #x78263ead7ee1e7e5) #x000007d9c152811e))
(constraint (= (f #x8e8e29c23c4e4e04) #x00007fffffffffff))
(constraint (= (f #xed992765b4354cc6) #x00007fffffffffff))
(constraint (= (f #x77b2e744c591e2c3) #x0000084d18bb3a6e))
(constraint (= (f #x762a7b60a0055b16) #x000009d5849f5ffa))
(constraint (= (f #x636d73ec76ea8ad2) #x00001c928c138915))
(constraint (= (f #xe8a05e6587933b68) #x00007fffffffffff))
(constraint (= (f #x5546b0ae5ad251ce) #x00007fffffffffff))
(constraint (= (f #x534d99a79abec9d9) #x00002cb266586541))
(constraint (= (f #xd2d04515b460e7e7) #x00002d2fbaea4b9f))
(constraint (= (f #x5e611ad270206c62) #x00007fffffffffff))
(constraint (= (f #xe34b2eced8540a42) #x00007fffffffffff))
(constraint (= (f #xda47539ea184067b) #x000025b8ac615e7b))
(constraint (= (f #x913e3b9eee5e8258) #x00006ec1c46111a1))
(constraint (= (f #x3c436ad52601a6c7) #x000043bc952ad9fe))
(constraint (= (f #x6b0e2e385daeb409) #x000014f1d1c7a251))
(constraint (= (f #x26b8be38e49e9e20) #x00007fffffffffff))
(constraint (= (f #x864b36a816d9e43e) #x000079b4c957e926))
(constraint (= (f #xe197e36ad89cb1b6) #x00001e681c952763))
(constraint (= (f #x01e4e98988027ae8) #x00007fffffffffff))
(constraint (= (f #x19c4b865b1c0dc25) #x0000663b479a4e3f))
(constraint (= (f #xee5ea7ec282c50b7) #x000011a15813d7d3))
(constraint (= (f #x48797a2c4ee72ee2) #x00007fffffffffff))
(constraint (= (f #xd74e4dadaeb9c818) #x000028b1b2525146))
(constraint (= (f #x077e937e20e7aa8d) #x000078816c81df18))
(constraint (= (f #xa830cad9b7026481) #x000057cf352648fd))
(constraint (= (f #xc7e22cdb8c69be90) #x0000381dd3247396))
(constraint (= (f #xc08dee2bdaa7ac7d) #x00003f7211d42558))
(constraint (= (f #x8ce36280ab4c4b79) #x0000731c9d7f54b3))
(constraint (= (f #xc13834d879085796) #x00003ec7cb2786f7))
(constraint (= (f #xd006bc5e5bb98ed3) #x00002ff943a1a446))
(constraint (= (f #x036dace46d8e6199) #x00007c92531b9271))
(constraint (= (f #x6d1bcccc9a8e5e01) #x000012e433336571))
(constraint (= (f #x90a09094d35b348e) #x00007fffffffffff))
(constraint (= (f #xd4bed645dee382b5) #x00002b4129ba211c))
(constraint (= (f #xd078a6ce5e5930b1) #x00002f875931a1a6))
(constraint (= (f #x76ead2e39ecce8ae) #x00007fffffffffff))
(constraint (= (f #xd982954b1e78c2cd) #x0000267d6ab4e187))
(constraint (= (f #x070e55ea185e5ec4) #x00007fffffffffff))
(constraint (= (f #x843ec5461626a2cb) #x00007bc13ab9e9d9))
(constraint (= (f #xb1c9aa431ec7d108) #x00007fffffffffff))
(constraint (= (f #x7e72e5d6a67e4783) #x0000018d1a295981))
(constraint (= (f #x21ed826c2e39b130) #x00005e127d93d1c6))
(constraint (= (f #x43a745c9eb786c6d) #x00003c58ba361487))
(constraint (= (f #x47966d7e7e5aeae8) #x00007fffffffffff))
(constraint (= (f #x7dc0eae8e6a8e0b9) #x0000023f15171957))
(constraint (= (f #xaac9b55e00d964b3) #x000055364aa1ff26))
(constraint (= (f #x66a95731c99ac49e) #x00001956a8ce3665))
(constraint (= (f #x612d71234ee838a3) #x00001ed28edcb117))
(constraint (= (f #xb322cae1c26ea705) #x00004cdd351e3d91))
(constraint (= (f #xc0766e6ae99dc384) #x00007fffffffffff))
(constraint (= (f #xeb3eebc138967bb5) #x000014c1143ec769))
(constraint (= (f #x22bee1ea953b2d08) #x00007fffffffffff))
(constraint (= (f #x85896e36985bacd9) #x00007a7691c967a4))
(constraint (= (f #x773a56cb3e60ea8c) #x00007fffffffffff))
(constraint (= (f #x2440766d3311e24c) #x00007fffffffffff))
(constraint (= (f #xeb7d7ce5a7ee6eda) #x00001482831a5811))
(constraint (= (f #x99c11bd9a40c9474) #x0000663ee4265bf3))
(constraint (= (f #x5ec15ea83044ecb6) #x0000213ea157cfbb))
(constraint (= (f #x76ee39c57eea1688) #x00007fffffffffff))
(constraint (= (f #x6578ec38352e255d) #x00001a8713c7cad1))
(constraint (= (f #xc3e688ea6918017e) #x00003c19771596e7))
(constraint (= (f #x9e9b270d111cdd4e) #x00007fffffffffff))
(constraint (= (f #x6452b6992de0545c) #x00001bad4966d21f))
(constraint (= (f #x3bcd7a87721ea652) #x0000443285788de1))
(constraint (= (f #xc1d45b1289037014) #x00003e2ba4ed76fc))
(constraint (= (f #xcda717e1e584e428) #x00007fffffffffff))
(constraint (= (f #x6195b9ab6ce37111) #x00001e6a4654931c))
(constraint (= (f #xec99b9ea580eee0b) #x000013664615a7f1))
(constraint (= (f #xee59648a81e9b030) #x000011a69b757e16))
(constraint (= (f #xe638b46e84dec81b) #x000019c74b917b21))
(constraint (= (f #xce1870ae0668504d) #x000031e78f51f997))
(constraint (= (f #x42a675e7d0e13a00) #x00007fffffffffff))
(constraint (= (f #xb8cb443e54d81920) #x00007fffffffffff))
(constraint (= (f #x843629230ec084ec) #x00007fffffffffff))
(constraint (= (f #xd74a49a83e240b96) #x000028b5b657c1db))
(constraint (= (f #xb6e39c678b63edb3) #x0000491c6398749c))
(constraint (= (f #x3ae59839e98475be) #x0000451a67c6167b))
(constraint (= (f #xac021aa95158e1ad) #x000053fde556aea7))
(constraint (= (f #x6e0bd9dad611849c) #x000011f4262529ee))
(constraint (= (f #xc4709ed398e82a4e) #x00007fffffffffff))
(constraint (= (f #x6e4858be15e02dec) #x00007fffffffffff))
(constraint (= (f #xec84e46e55381282) #x00007fffffffffff))
(constraint (= (f #x69bab76d3b56c07e) #x000016454892c4a9))
(constraint (= (f #x09a488aae0ced4da) #x0000765b77551f31))
(constraint (= (f #x0bcb392e2e24cec5) #x00007434c6d1d1db))
(constraint (= (f #x4c5b67dc968326a3) #x000033a49823697c))
(constraint (= (f #x2db38a89a7bd3e98) #x0000524c75765842))
(constraint (= (f #x3cada680ecae6366) #x00007fffffffffff))
(constraint (= (f #x70c0820908384d49) #x00000f3f7df6f7c7))
(constraint (= (f #x2b2c7581d649e06e) #x00007fffffffffff))
(constraint (= (f #x6897e0d496c12606) #x00007fffffffffff))
(constraint (= (f #x79ebadbe786b2e75) #x0000061452418794))
(constraint (= (f #x49207ee0c0a3c865) #x000036df811f3f5c))
(constraint (= (f #xdda1ad55bb81bbb4) #x0000225e52aa447e))
(constraint (= (f #x44e9e828c07579e8) #x00007fffffffffff))
(constraint (= (f #x761e1eccbb8953dc) #x000009e1e1334476))
(constraint (= (f #x7e91d32e94b3be49) #x0000016e2cd16b4c))
(constraint (= (f #x306301c5ee319ae3) #x00004f9cfe3a11ce))
(constraint (= (f #xe9ee14ede8e63425) #x00001611eb121719))
(check-synth)
