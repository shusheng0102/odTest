### **Highlight**

* **特征序列化：** 将所有的 id / categorical 特征做成一个序列，丢弃所有的数值特征。**并将召回和排序统一定义为序列建模任务。**
* **模型结构：采用 HSTU（Hierarchical Sequential Transduction Units）结构** ，在 8192 长度的序列上相比于 FlashAttention2 实现了 **5.3x** 到 **15.2x** 的加速； **采用 M-FALCON 算法分担计算开销** ，能够在相同的推理开销下，服务于 **285x** 复杂的模型，同时实现 **1.50x** 到 **2.48x** 的加速。
* **模型效果：** 在工业级别的[推荐系统](https://so.csdn.net/so/search?q=%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9F&spm=1001.2101.3001.7020)上，能够分别提升召回 / 排序阶段的在线指标 **6.2%** 和  **12.4%** 。
* **验证了 LLM 中的 scaling law 也可能适用于大规模推荐系统。**

建设数十亿规模的推荐系统面临三个挑战：

* **推荐系统中的特征并没有明确的结构。** 通常包含类别特征和数字特征。
* **推荐系统使用不断更新的数十亿级的词汇表。** 相比之下，语言仅仅包含数十万级别的静态词汇。
* **计算成本是实现大规模序列模型的主要瓶颈。** GPT-3 用 1-2 个月的时间在数千个 GPU 对 300B 的 token 进行了训练。而推荐系统需解决数十亿的日活用户和数十亿的内容信息，在**一天内需处理的 token** 比语言模型在一到两个月内要处理的要 **高几个数量级** 。

![aa24ad0c6f8fd84a6dd81692c0c20ee4.png](https://img-blog.csdnimg.cn/img_convert/aa24ad0c6f8fd84a6dd81692c0c20ee4.png)

### **如何实现特征统一？**

* **Categorical（'sparse'）特征：进行序列化**
  * 选取最长的时间序列（通常是将用户交互的 item 合并）作为主要的时间序列。
  * 其余的特征是随着时间缓慢变化的时间序列，例如用户关注的创作者等。通过保留每个连续片段最早的条目来压缩这些时间序列，并将结果合并到主序列中。
* **Numerical（'dense'）特征：直接丢弃**
  * 这类特征变化更为频繁，从计算和存储的角度将这些特征完全[序列化](https://so.csdn.net/so/search?q=%E5%BA%8F%E5%88%97%E5%8C%96&spm=1001.2101.3001.7020)是不可行的。
  * 这些数值特征是由类别特征聚合而来，而这些类别特征我们已经编码入了模型。

**通过这种设计，可以有效降低序列的长度。**

![8b7007ce7c4b71cfd5ab803f04db7a11.png](https://img-blog.csdnimg.cn/img_convert/8b7007ce7c4b71cfd5ab803f04db7a11.png)

![2cfd465eba4aef845bb4467f72477d8c.png](https://img-blog.csdnimg.cn/img_convert/2cfd465eba4aef845bb4467f72477d8c.png)

### **将召回和排序定义为序列建模任务**

### 给定上文得到的时间序列 ，这些 token 对应的时间 ，**如果 ****表示内容，则还有用户在 ** **上的行为 **  **。** 我们可以将召回和排序定义为序列建模任务，根据 mask sequence 将输入序列映射为输出序列 ， 代表 没有定义。召回和排序阶段都以 causal masked autoregressive 的方式进行训练。这些输入 token 都来自一个动态词表 ，其中内容集合为 。

#### 

#### **2.1 召回**

召回任务为每个用户 学习分布 ，其中 。训练目标函数是选择 来最大化某个特定的回报。这与标准的自回归目标函数有一些区别：

* **监督信号并不一定是 **  **，** 因为用户对 不一定是正面反馈。
* 当序列的下一个 token 不是表示内容（）的时候，。

#### **2.2 排序**

#### 目前的推荐系统需要  **'target-aware' formulation** ，即需要预测目标 和用户行为在早期进行交互。然而在经典的自回归模型中，交互通常发生得较晚（在 softmax 之后）。**因此我们通过将主时间序列中的内容 ****和行为 ** **进行交错来解决这个问题，** 形成 的序列（如果不考虑 ），在 action 的位置 。之后在表示内容的 token 后接神经网络进行多任务预测。

#### 代表输出的 token 未定义，即不计算损失。这里 mask sequence 的设定的区别主要是由于召回和排序阶段的目标不同造成的。召回阶段的主要目标是根据之前的内容预测下一个内容，因此当序列的下一个 token 不是表示内容（）的时候，。

#### 

#### 而排序阶段的主要目标为对内容进行多任务预测（ctr、cr），因此在 action 的位置 ，在表示内容的 token 后接神经网络进行多任务预测；同时也可以利用自回归损失进行计算， 的下一个为 ，而 的下一个为 。这样在 的位置设置 mask=0 很合理。

![4aa6d362659179103e5a3be69e0f95f8.png](https://img-blog.csdnimg.cn/img_convert/4aa6d362659179103e5a3be69e0f95f8.png)

### **训练方式是怎样的？**

### 在目前流式计算的场景下以 self-attention 为核心的模型复杂度为 ，其中 是用户 的 token 数量， 是 embedding 的维度，隐藏层大小 。令 ，则计算复杂度为 。

**生成式训练可将计算复杂度降低一个数量级。** 对第 个用户以 的速率降采样，训练的总计算量变成了 。如果把降采样率设置为 ，则复杂度可降低到 。在工业场景的系统中，通常在用户请求或 session 结束时发送训练样本，对应到采样率就是 。

![b8d743091654c4b7fe82c0387f3c540d.png](https://img-blog.csdnimg.cn/img_convert/b8d743091654c4b7fe82c0387f3c540d.png)

### **模型结构**

在模型上采用了 HSTU（Hierarchical Sequential Transduction Unit） 的结构，每层 HSTU 由三个部分组成：

![4c4cd2891789276964ef139e15b40baf.png](https://img-blog.csdnimg.cn/img_convert/4c4cd2891789276964ef139e15b40baf.png)

其中 为 MLP，这里使用了单层线性层，即 。 和 为非线性层，这里使用了 SiLU。 为包含了位置 和时间 的 relative attention bias，并且引入了 layernorm 以提高训练稳定性。

**特征抽取（Feature extraction）：** 目前主流模型中的特征抽取部分主要采用了 DIN 的方式，即 pairwise attention and target-aware pooling，这部分可以通过公式（2）进行建模。在传统 Q, K, V 基础上，多了一个 U，即上文 中的 ，用以压缩用户信息，可以理解为底层的用户长期行为序列表征，同时保留一些底层信息。

**特征交叉（Feature interaction）：** HSTU 通过 attention 抽取出的特征 与 进行元素积的形式，实现了特征交叉。文章采用 SiLU 代替了 softmax，这个处理和 DIN 是类似的，将序列维度的聚合权重 的约束放松了，更好地保留用户兴趣的强度。

没有使用 softmax：一个是包含强度的特征经过 softmax 之后会变弱，一个是 softmax 虽然鲁棒性更好，但不适合流式更新场景。

**特征变换（Representation transformation）：** 当下模型通常使用 MoE 的方式实现特征的转换，而公式（3）中的元素积便可以实现 MoE 中的门机制。也有点像 SENet / LHUC 等特征重要度学习方法。

整体上是融合借鉴了 DIN、MoEs、LHUC 等工作的思想，在 Transformer 框架内做一些推荐领域特定的适配。

![c6310b69d5f1170a90d2db074c979433.png](https://img-blog.csdnimg.cn/img_convert/c6310b69d5f1170a90d2db074c979433.png)

### **一些工程上的优化**

#### **5.1 利用稀疏性**

利用输入序列的稀疏性，为 GPU 开发了一种高效的 attention kernel，以类似于 FlashAttention 的方式融合 back-to-back GEMMs，这个设计提升了 2-5x 的吞吐量。

#### **5.2 增加稀疏性**

#### 使用 **随机长度（Stochastic Length, SL）** 算法，可以进一步提高用户序列的稀疏性。用户历史序列的一个特点是用户行为在时间上具有重复性，可以将输入序列按下面的规则进行截断。 是一个函数，从长度为 的原始序列中选取长度 的子序列。这种方法将 attention 的复杂度降低到 。

![773170f95a627d59458fd67f38f1bd7b.png](https://img-blog.csdnimg.cn/img_convert/773170f95a627d59458fd67f38f1bd7b.png)

#### **5.3 降低内存使用量**

推荐系统使用较大的 batch size，activation memory usage 成为瓶颈。HSTU 的设计（将线性层减少为两层、将多个计算融合为一个运算）可将 activation memory usage 降低至 14d，而 Transformer 为 33d。使用 rowwise AdamW 优化器，并且将优化器状态放在 DRAM 上，从而将每个浮点数的 HBM 使用量从 12 字节减少到 2 字节。

#### **5.4 通过成本摊销扩大推理规模**

#### 推荐系统在推理时需要处理大量的候选信息，在排序阶段一般是万的量级。使用 M-FALCON 算法 ，将总共 个候选分为大小为 的 mini-batch 以利用编码器级 KV 缓存，并通过修改 attention masks 和 biases 的方式，同时处理 个候选。M-FALCON 算法使模型复杂度随候选数量线性增加，在推理资源不变的情况下，以 1.5 倍的吞吐量落地了复杂度 285 倍的模型。

![10ae67806c723a0dbe1fa18880274a05.png](https://img-blog.csdnimg.cn/img_convert/10ae67806c723a0dbe1fa18880274a05.png)

### **实验效果如何？**

**模型参数：** 使用了 100B 的训练样本， 64-256 块 H100 。

* 召回：l=6, n=512, d=256
* 排序：l=3, n=2048, d=512

**Baseline：排序部分**采用了 1000 个dense特征，50 个稀疏特征，采用 MoE、DCN V2、DIN、residual connection 等技术；**召回部分**采用了双塔模型，in-batch and out-of-batch 采样，输入特征包括 id、稀疏特征等。通过残差连接 MLP 将输入压缩成 user 和 item 表征。

排序指标使用了 Normalized Entropy（NE）， **NE 下降 0.001 可以认为是显著的，通常会带来线上 0.5% 的总线指标提升。** E-Task 是在线参与度指标，例如点赞、转发等。C-Task 是例如完播，时长这样的任务。

在工业规模的流式设置下，生成式推荐模型（GR）与经典推荐模型（DLRM）的效果比较，其中 DLRM（abl.features）是将 GR 模型的输入的相对原始的特征输入给 DLRM；GR（content-based）是仅使用内容相关的 feature，说明了用户行为建模的重要性；GR（interactions only）是仅仅考虑用户互动的 item，只关注用户的正样本行为，不考虑负样本，比如曝光未点击之类的不作为序列构成；GR（new source）是指 GR 模型作为一个新的召回源；GR（replace source）指 GR 模型代替原有的召回源。

![aa449bb10ab0a50871d1186ae8496fa5.png](https://img-blog.csdnimg.cn/img_convert/aa449bb10ab0a50871d1186ae8496fa5.png)

文章其次比较了 GR 与 DLRM 的效率。尽管 GR 模型在 FLOP 方面要复杂 285 倍，但由于 HSTU 结构和 M-FALCON 算法，在 1024 / 16384 个候选项时分别实现了 1.50x / 2.48x 的吞吐量。

![fc3b94035da0d5edbcab6f72c6811def.png](https://img-blog.csdnimg.cn/img_convert/fc3b94035da0d5edbcab6f72c6811def.png)

可扩展性（scalibility）：文章最后展示了 LLM 中的 scaling law 也可能适用于大规模推荐系统。

![13b7b028be1c0b44eb3aaf0c41559611.png](https://img-blog.csdnimg.cn/img_convert/13b7b028be1c0b44eb3aaf0c41559611.png)

实验关注了召回的 Hit Rate@100 和 Hit Rate@500，以及排序的 NE 指标，与计算量呈现出幂律 scaling 趋势。作者在三个量级上做了该观测，最大的模型达到序列长度为8,192，嵌入维度为1,024，HSTU 24层。此时总计算量接近于 GPT-3 和 LLaMA2。

此外文章提到，不同于 LLMs，序列长度对 GRs 来说更重要。 更长的序列能够捕捉更多的上下文和依赖关系，从而表现更好。因此在可能的情况下，扩大序列长度是很重要的。通过序列长度、embedding 维数等能够实现 GRs 模型的 scaling。

![2803c87967882e6be50278bc3a9ae5df.png](https://img-blog.csdnimg.cn/img_convert/2803c87967882e6be50278bc3a9ae5df.png)

### **总结**

文章提出了首个生成式推荐系统模型，实现了 LLM + rec 的有机结合方案，在 Transformer 框架内巧妙融合了推荐系统的很多经典设计，无疑是**一篇开创性的工作。**

在核心产品线替换掉了近十年工业界长期使用的基于海量异构特征的深度推荐模型，并且验证了推荐系统领域中的 scaling law，为各大厂提供了一条可靠的路径参考。

但同时，目前模型仍是基于 ID 体系进行学习的，并没有多模态信息的引入。众所周知 Transformer 在融合多模态方面有着得天独厚的优势，如果引入多模态信息是否会得到进一步的提升？

能否将召回和排序任务通过损失函数进行统一，实现一段式推荐模型也是未来值得探索的方向。
